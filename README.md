The Problem: Lack of Standardized Tool Execution Protocols

The agentic AI community currently struggles with a fragmented landscape for tool execution. Developers face challenges with:
1.  **Inconsistent Tool Calling:** Different LLM providers and agentic frameworks have their own conventions for describing and invoking tools, leading to significant boilerplate and integration headaches.
2.  **Lack of Lazy Result Loading:** Tools often return large or complex results. Immediate, synchronous loading can be inefficient, especially for server-side invocations or when only parts of the result are needed.
3.  **Difficulty with Custom Code Execution:** Integrating arbitrary, potentially long-running custom code as tools is cumbersome and lacks standardized patterns for managing execution and result retrieval.

This project, `AgentToolKit`, addresses these issues by proposing a **standardized, provider-agnostic protocol for tool definition and execution**, with native support for lazy result loading and an emphasis on asynchronous, stream-friendly operations.

Why this project shape/stack was chosen:

We chose a **Python package** with a clear **API specification** and a **reference implementation**.
*   **Python:** The dominant language in the AI/ML community, making it accessible for most agent developers.
*   **Package Structure:** Allows for easy installation, dependency management, and clear separation of concerns (protocol definition, executor implementation, client-side integration).
*   **API Specification (Pydantic):** Provides a strong, type-safe contract for tool definitions and execution requests/responses, making it easy for different frameworks or LLM providers to generate or consume these structures.
*   **Reference Implementation:** Demonstrates how the protocol can be used to build a robust tool execution system, focusing on asynchronous execution and lazy result loading.

Setup and Usage (Zero API keys required):

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-org/agenttoolkit.git
    cd agenttoolkit
    ```
2.  **Install dependencies:**
    ```bash
    pip install -e .
    ```
3.  **Run the example:**
    The example demonstrates defining a tool, executing it asynchronously, and lazily loading its results using fixture data.

    ```bash
    python demo.py
    ```

    You will see output demonstrating:
    *   A simulated LLM generating a `ToolExecutionRequest`.
    *   The `ToolExecutor` receiving the request and simulating execution.
    *   The client receiving an `ExecutionResult` with a `result_uri`.
    *   Lazy loading of the actual tool output from the `result_uri`.

Optional Real-LLM Adapter:

This prototype focuses purely on the tool execution protocol and does not involve direct LLM interaction in its core logic. Therefore, there is no optional real-LLM adapter in this specific project. The protocol is designed to be consumed *by* an LLM orchestrator, not to *be* one.
