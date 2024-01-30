from langchain.docstore import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from typing import Optional
from langchain.prompts import PromptTemplate
from langchain_experimental.autonomous_agents import BabyAGI
from langchain_openai import OpenAIEmbeddings
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent
from langchain.chains import LLMChain
from langchain_community.utilities import SerpAPIWrapper
from langchain_openai import OpenAI
import faiss
import io
import contextlib
import re

def generateAgentAnswer(user_input):
    # Create a string buffer to capture output
    buffer = io.StringIO()

    # Redirect stdout to the buffer
    with contextlib.redirect_stdout(buffer):
        # Define your embedding model
        embeddings_model = OpenAIEmbeddings()
        embedding_size = 1536
        index = faiss.IndexFlatL2(embedding_size)
        vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})
        todo_prompt = PromptTemplate.from_template("You are a planner who is an expert at coming up with a todo list for a given objective. Come up with a todo list for this objective: {objective}")
        todo_chain = LLMChain(llm=OpenAI(temperature=0), prompt=todo_prompt)
        search = SerpAPIWrapper()
        tools = [
            Tool(name="Search", func=search.run, description="useful for when you need to answer questions about current events"),
            Tool( name="TODO", func=todo_chain.run, description="useful for when you need to come up with todo lists. Input: an objective to create a todo list for. Output: a todo list for that objective. Please be very clear what the objective is!"),
        ]
        prefix = """You are an AI who performs one task based on the following objective: {objective}. Take into account these previously completed tasks: {context}."""
        suffix = """Question: {task} {agent_scratchpad}"""
        prompt = ZeroShotAgent.create_prompt(tools, prefix=prefix, suffix=suffix, input_variables=["objective", "task", "context", "agent_scratchpad"])
        llm = OpenAI(temperature=0)
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        tool_names = [tool.name for tool in tools]
        agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
        agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

        OBJECTIVE = user_input

        # Logging of LLMChains
        verbose = False
        # If None, will keep on going forever
        max_iterations: Optional[int] = 3
        baby_agi = BabyAGI.from_llm(llm=llm, vectorstore=vectorstore, task_execution_chain=agent_executor, verbose=verbose, max_iterations=max_iterations)
        baby_agi({"objective": OBJECTIVE})

    # buffer contains all data
    output = buffer.getvalue()

    cleaned_output = re.sub(r'\x1b\[\d+(;\d+)*m', '', output)
    # Optionally, replace "\n" with actual new lines if needed, or handle other specific replacements

    return cleaned_output