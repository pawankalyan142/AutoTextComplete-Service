import logging
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from constants import api_key

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize LLM with llama-3.3-70b-versatile
model_name = "llama-3.3-70b-versatile"
groq_chat = ChatGroq(groq_api_key=api_key, model_name=model_name)

# Memory for last 'k' exchanges
conversational_memory = ConversationBufferWindowMemory(
    memory_key="chat_history",  # Key must match the input variable in the prompt template
    input_key="problem_statement",  # Specify key for normal input outside memory
    return_messages=True,
    k=100
)

# Troubleshooting prompt
troubleshooting_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are an expert troubleshooting assistant. Given a problem statement and conversation history, provide clear, actionable troubleshooting steps, and platform-specific commands to help resolve the issue. Always provide commands for Windows, macOS, and Linux whenever relevant."),
    HumanMessagePromptTemplate.from_template(
        "Problem: {problem_statement}\n\n"
        "Previous Conversations: {chat_history}\n\n"
        "Commands and Suggestions for Resolution (including for Windows, macOS, and Linux where applicable):"
    )
])


# Create the chain with memory and correct variable mapping
conversation_chain = ConversationChain(
    prompt=troubleshooting_prompt,
    llm=groq_chat,
    memory=conversational_memory,
    input_key="problem_statement"  # Specify how the chain receives the problem statement input
)

def generate_troubleshooting_steps(problem_statement: str) -> str:
    """
    Generate troubleshooting steps based on the provided problem statement, considering past conversations.

    :param problem_statement: The issue description provided by the user.
    :return: A step-by-step troubleshooting guide.
    """
    try:
        # Invoke the chain
        response = conversation_chain.run(problem_statement=problem_statement)
        
        logging.info(f"Generated troubleshooting steps for problem: {problem_statement}")
        return response
    except Exception as e:
        logging.error(f"Error generating troubleshooting steps: {str(e)}")
        return "An error occurred while generating troubleshooting steps."
