import asyncio
import json
from pathlib import Path
from typing import Dict, Any

from agenttoolkit.protocol import ToolDefinition, ToolExecutionRequest, ExecutionResult
from agenttoolkit.executor import ToolExecutor

# --- Define tool handlers ---
def handle_search_web(args: Dict[str, Any]) -> Dict[str, Any]:
    query = args.get("query")
    print(f"[TOOL] Executing search_web for query: '{query}'")
    # Simulate a real API call or complex logic
    return {
        "results": [
            {"title": f"AI Breakthrough: {query} - Article 1", "url": "http://example.com/ai1"},
            {"title": f"The Future of {query} - Research Paper", "url": "http://example.com/ai2"},
        ],
        "summary": f"Found several articles related to '{query}'.",
        "query_echo": query # Include query to verify arguments
    }

def handle_get_weather(args: Dict[str, Any]) -> Dict[str, Any]:
    city = args.get("city")
    unit = args.get("unit", "celsius")
    print(f"[TOOL] Executing get_weather for city: '{city}', unit: '{unit}'")
    # Simulate fetching weather from an external service
    return {
        "city": city,
        "temperature": {"value": 25, "unit": unit} if unit == "celsius" else {"value": 77, "unit": unit},
        "conditions": "Sunny",
        "forecast": "Clear skies tomorrow"
    }

async def main():
    print("AgentToolKit Demo: Standardized Tool Execution Protocol")
    print("------------------------------------------------------\n")

    # 1. Load Tool Definitions from fixture
    print("Loading tool definitions...")
    tools_fixture_path = Path(__file__).parent / "fixtures" / "tools.json"
    with open(tools_fixture_path, "r") as f:
        tool_defs_raw = json.load(f)
    
    tool_definitions = {td["name"]: ToolDefinition(**td) for td in tool_defs_raw}
    print(f"Loaded {len(tool_definitions)} tools: {list(tool_definitions.keys())}\n")

    # 2. Initialize ToolExecutor and register handlers
    print("Initializing ToolExecutor and registering handlers...")
    executor = ToolExecutor(tool_definitions)
    executor.register_handler("search_web", handle_search_web)
    executor.register_handler("get_weather", handle_get_weather)
    print("Executor ready.\n")

    # 3. Simulate an LLM generating a ToolExecutionRequest
    print("Simulating LLM generating a ToolExecutionRequest (from fixture)...")
    llm_payload_path = Path(__file__).parent / "fixtures" / "llm_tool_call_payload.json"
    with open(llm_payload_path, "r") as f:
        llm_request_raw = json.load(f)
    
    # Parse the raw payload into our standardized protocol object
    llm_tool_request = ToolExecutionRequest(**llm_request_raw)
    print(f"LLM wants to execute tool '{llm_tool_request.tool_name}' with arguments: {llm_tool_request.arguments}")
    print(f"Request ID: {llm_tool_request.request_id}\n")

    # 4. Executor receives and processes the request
    print(f"Executor receiving request {llm_tool_request.request_id}...")
    execution_result: ExecutionResult = await executor.execute_tool(llm_tool_request)
    print(f"Executor returned result (status: {execution_result.status.value}) for request {execution_result.request_id}.")
    
    if execution_result.status == ExecutionStatus.COMPLETED:
        print(f"Result URI: {execution_result.result_uri}")
        # 5. Agent (or client) lazily loads the result data using the URI
        print("\nAgent/Client side: Lazily loading tool output from result_uri...")
        try:
            tool_output = await executor.get_result_data(execution_result.result_uri)
            print("\n--- Lazily Loaded Tool Output ---")
            print(json.dumps(tool_output, indent=2))
            print("---------------------------------\n")

            # Verify lazy loaded content
            assert tool_output["query_echo"] == llm_tool_request.arguments["query"]
            print("Successfully loaded and verified tool output.")

        except Exception as e:
            print(f"Failed to lazily load result: {e}")
    else:
        print(f"Tool execution failed: {execution_result.error_message}")

    print("\n--- Demonstrating another tool execution (get_weather) ---")
    weather_request = ToolExecutionRequest(
        tool_name="get_weather",
        arguments={"city": "London", "unit": "fahrenheit"},
        request_id="llm_req_weather_001"
    )
    print(f"LLM wants to execute tool '{weather_request.tool_name}' with arguments: {weather_request.arguments}")
    weather_execution_result = await executor.execute_tool(weather_request)
    print(f"Executor returned result (status: {weather_execution_result.status.value}) for request {weather_execution_result.request_id}.")
    
    if weather_execution_result.status == ExecutionStatus.COMPLETED:
        print(f"Result URI: {weather_execution_result.result_uri}")
        print("\nAgent/Client side: Lazily loading weather tool output...")
        try:
            weather_output = await executor.get_result_data(weather_execution_result.result_uri)
            print("\n--- Lazily Loaded Weather Output ---")
            print(json.dumps(weather_output, indent=2))
            print("------------------------------------\n")
        except Exception as e:
            print(f"Failed to lazily load weather result: {e}")
    else:
        print(f"Weather tool execution failed: {weather_execution_result.error_message}")


if __name__ == "__main__":
    asyncio.run(main())
