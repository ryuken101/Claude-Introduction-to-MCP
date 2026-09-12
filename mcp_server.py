# Import the Python MCP SDK and then initialise the server
from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")

# Documents are stored in a dictionary 
docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures",
    "outlook.pdf": "This document presents the projected future performance of the system",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment"
}

# So essentially, the SDK uses decorators for defining tools 
# Instead of writing JSON schemas manually, you can use Python type hints and field descriptions. 
# The SDK automatically generates the proper schema that Claude can understand.


# Creating a Document Reader Tool 

# The first tool reads document contents by ID

# Decorator specifies the tool name & desc
@mcp.tool (
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)

# Field class from Pydantic provides argument descriptions that help Claude 
# Understand what each parameter expects 
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs: 
        raise ValueError(f"Doc with id {doc_id} not found")

    return docs[doc_id]

# Second tool performs simple find-and-replace operations on documents 
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)

# Tool takes 3 parameters: the document ID, the text to find, and the replacement text
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)