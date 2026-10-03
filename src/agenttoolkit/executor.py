import asyncio
import json
from typing import Any, Callable, Dict, Optional
from urllib.parse import urlparse
import httpx
import anyio

from agenttoolkit.protocol import (
    ToolDefinition,
    ToolExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
)

class ToolExecutor:
    """
    A reference implementation of a tool executor that simulates asynchronous
    tool execution and lazy result loading.
    """
    def __init__(self, tools: Dict[str, ToolDefinition]):
        self._tools = {tool.name: tool for tool in tools.values()}
        self._execution_handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self._result_store: Dict[str, Any] = {} # In-memory store for demonstration

    def register_handler(self, tool_name: str, handler: Callable[[Dict[str, Any]], Any]):
        """Registers a Python function as the handler for a given tool."""
        if tool_name not in self._tools:
            raise ValueError(f"Tool '{tool_name}' not defined.")
        self._execution_handlers[tool_name] = handler

    async def execute_tool(self, request: ToolExecutionRequest) -> ExecutionResult:
        """
        Executes a tool based on the provided request, returning an ExecutionResult
        with a result_uri for lazy loading.
        """
        tool_def = self._tools.get(request.tool_name)
        if not tool_def:
            return ExecutionResult(
                request_id=request.request_id,
                status=ExecutionStatus.FAILED,
                error_message=f"Tool '{request.tool_name}' not found."
            )

        handler = self._execution_handlers.get(request.tool_name)
        if not handler:
            return ExecutionResult(
                request_id=request.request_id,
                status=ExecutionStatus.FAILED,
                error_message=f"No handler registered for tool '{request.tool_name}'."
            )

        try:
            # Simulate async execution
            await asyncio.sleep(0.1) # Simulate some work

            # Execute the actual tool logic
            raw_output = await anyio.to_thread.run_sync(handler, request.arguments)

            # Store the result and generate a result_uri
            result_key = f"result_{request.request_id}"
            self._result_store[result_key] = raw_output
            result_uri = f"http://localhost:8000/results/{result_key}" # Mock HTTP endpoint

            result = ExecutionResult(
                request_id=request.request_id,
                status=ExecutionStatus.COMPLETED,
                result_uri=result_uri,
                direct_output=None # For demonstration, we'll always use lazy loading
            )

            # If a callback_uri is provided, notify the caller (simulated)
            if request.callback_uri:
                print(f"Simulating callback to {request.callback_uri} with result for {request.request_id}")
                # In a real system, this would be an actual HTTP POST or message queue push
                # async with httpx.AsyncClient() as client:
                #     await client.post(str(request.callback_uri), json=result.model_dump())

            return result
        except Exception as e:
            return ExecutionResult(
                request_id=request.request_id,
                status=ExecutionStatus.FAILED,
                error_message=str(e)
            )

    async def get_result_data(self, result_uri: str) -> Any:
        """
        Simulates lazy loading of result data from a URI.
        In a real system, this would involve an HTTP GET, S3 download, etc.
        """
        parsed_uri = urlparse(result_uri)
        if parsed_uri.scheme == "http" and parsed_uri.netloc == "localhost:8000":
            path_parts = parsed_uri.path.strip("/").split("/")
            if len(path_parts) == 2 and path_parts[0] == "results":
                result_key = path_parts[1]
                if result_key in self._result_store:
                    print(f"Lazily loading result data for {result_key}...")
                    await asyncio.sleep(0.05) # Simulate network latency
                    return self._result_store[result_key]
        raise ValueError(f"Could not retrieve result from URI: {result_uri}")
