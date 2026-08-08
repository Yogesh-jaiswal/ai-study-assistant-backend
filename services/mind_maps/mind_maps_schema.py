from pydantic import BaseModel, Field

class MindMapNode(BaseModel):
    id: str = Field(description="Unique identifier of each node.")
    label: str = Field(description="Content of the node.")
    parent_id: str | None = Field(
        default=None,
        description="Parent node's id to create heirarchical structure (Optional for the root node)."
    )


class MindMapResponse(BaseModel):
    title: str = Field(
        description="A short descriptive title summarizing the topic."
    )
    nodes: list[MindMapNode] = Field(
        description="List of all the nodes.",
        max_length=50
    )