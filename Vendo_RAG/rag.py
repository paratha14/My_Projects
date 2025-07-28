from prompts import get_prompt
from model import get_model, get_parser

def build_rag_chain():
    model = get_model()
    parser = get_parser()
    prompt = get_prompt(parser.get_format_instructions())
    chain= prompt | model | parser
    return chain
