from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_exa import ExaSearchRetriever, TextContentsOptions
from langchain_openai import ChatOpenAI
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import DuckDuckGoSearchRun

def returnAllSearchRestults(userSearch):
    # Exa Search
    retriever = ExaSearchRetriever(k=1, text_contents_options=TextContentsOptions(max_length=100))
    prompt = PromptTemplate.from_template(
        """Answer the following query based on the following context:
            query: {query}
            <context>
            {context}
            </context
        """
    )

    llm = ChatOpenAI(model="gpt-3.5-turbo-1106")

    chain = ( RunnableParallel({"context": retriever, "query": RunnablePassthrough()}) | prompt | llm )

    exa_response = str(chain.invoke(userSearch))

    # DuckDuckGo Search
    search = DuckDuckGoSearchRun()
    duckduckgoResult = search.run(userSearch)

    # Wikipedia Search
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    wikiResult = wikipedia.run(userSearch)

    return exa_response, duckduckgoResult, wikiResult

