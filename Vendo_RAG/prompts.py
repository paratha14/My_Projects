from langchain_core.prompts import PromptTemplate

def get_prompt(format_instructions):
    return PromptTemplate(
        template="""You are an expert supplier-matching assistant.

Given:
Vendor's Information: {vendor_info}

Search the context for a supplier that:
1. Offers **at least one** of the required items
2. Has **matching or nearby location** preference
3. Has **trust score** closer to 1.0 (ideal)

Give at least 2 suppliers based on trust score and item overlap.

Reply only using this JSON format:
{format_instructions}

Context:
{supp_info}

If no match is found, return this exact JSON:
{{
  "supplier_name": "No suitable suppliers found",
  "items_matched": [],
  "location": "",
  "trust_score": 0.0
}}""",
        input_variables=["vendor_info", "supp_info"],
        partial_variables={"format_instructions": format_instructions}
    )
