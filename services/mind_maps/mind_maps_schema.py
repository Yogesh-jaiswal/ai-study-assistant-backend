from pydantic import BaseModel, Field

class MindMapNode(BaseModel):
    """Schema representing a single min map node."""
    label: str = Field(..., description="The main content of the mind map node.")
    children: list["MindMapNode"] = Field(default_factory=list, description="List of childrens of the node using the recursive structure.")

class MindMapResponse(BaseModel):
    """Schema representing generated mind map."""
    title: str = Field(..., description="A short descriptive title summarizing the quiz topic.")
    root: MindMapNode = Field(..., description="The root node of the generated mind map.")