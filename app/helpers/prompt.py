from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.prompts import ChatPromptTemplate
from llama_index.core.memory import BaseMemory
# memory=BaseMemory()
language= 'French'
# Text QA Prompt
chat_text_qa_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content=(
            """ 
            You are an experienced immigration lawyer providing detailed legal advice in {language}. 
            Carefully review the following documents to extract relevant information and address the client's question 
            Analyze any legal regulations, risks, or implications that may apply, and provide guidance on the next steps.

                Instructions:
                1. Identify key legal issues or relevant regulations from the provided documents.
                2. Explain how the information applies to the client’s situation.
                3. Highlight any significant risks, legal obligations, or considerations the client should be aware of.
                4. Offer clear advice on the next steps, considering short-term and long-term outcomes.
                5. Note any additional documentation, evidence, or forms the client should prepare

                Please provide a structured and thorough response, clearly addressing each point in a way that helps the client understand their legal standing and options in {language}.
            """
        ),
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=(
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "answer the query.\n"
            "Query: {query_str}\n"
            "Answer: "
        ),
    ),
]

text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)

# Refine Prompt
chat_refine_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content=(
            "You are an expert Q&A system that strictly operates in two modes "
            "when refining existing answers:\n"
            "1. **Rewrite** an original answer using the new context.\n"
            "2. **Repeat** the original answer if the new context isn't useful.\n"
            "Never reference the original answer or context directly in your answer.\n"
            "When in doubt, just repeat the original answer."
        ),
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=(
            "New Context: {context_msg}\n"
            "Query: {query_str}\n"
            "Original Answer: {existing_answer}\n"
            "New Answer: "
        ),
    ),
]
refine_template = ChatPromptTemplate(chat_refine_msgs)