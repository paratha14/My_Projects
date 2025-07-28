from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class SupplierMatch(BaseModel):
    suppliers: list[dict] = Field(description="List of best-matching suppliers")
    items_matched: list[str] = Field(description="Items matched")
    location: str = Field(description="Location")
    trust_score: float = Field(description="Trust score (0–1)")

def get_model():
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.8)

def get_parser():
    return JsonOutputParser(pydantic_object=SupplierMatch)
