from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, HttpUrl, parse_obj_as

class ToolParameter(BaseModel):
    name: str
    type: str = "string" # e.g., "string", "integer", "boolean", "object", "array"
    description: Optional[str] = None
    required: bool = False
    # For object types, define nested properties here
    properties: Optional[Dict[str, 'ToolParameter']] = None
    items: Optional['ToolParameter'] = None # For array types

class ToolDefinition(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: List[ToolParameter] = Field(default_factory=list)
    # The URI where the tool's execution handler can be invoked
    # This might be a local path, a REST endpoint, a message queue topic, etc.
    execution_uri: str

class ToolExecutionRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    request_id: str = Field(default_factory=lambda: f"req_{hash(f'{ToolExecutionRequest.__qualname__}{__import__('uuid').uuid4()}')}")
    # Optional: Callback URI for async result notification
    callback_uri: Optional[HttpUrl] = None

class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ExecutionResult(BaseModel):
    request_id: str
    status: ExecutionStatus
    # A URI pointing to the actual result data.
    # This enables lazy loading and streaming of potentially large results.
    result_uri: Optional[HttpUrl] = None
    error_message: Optional[str] = None
    # For very small results, or initial status updates, direct data can be included
    direct_output: Optional[Any] = None

# Update ToolParameter to support recursive definition
ToolParameter.model_rebuild()
