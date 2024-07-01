from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_community.vectorstores import Chroma
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from dotenv import load_dotenv
load_dotenv()


class ChatAI:

    def __init__(self):
        self.model = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.embeddings = OpenAIEmbeddings()
        self.search_tool = TavilySearchResults()
        instructions = """You are an assistant."""
        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        self.prompt = base_prompt.partial(instructions=instructions)
        self.tools = [self.search_tool]

    def ingest(self, file_path: str):
        docs = PyPDFLoader(file_path=file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)
        vector_store = Chroma.from_documents(documents=chunks, embedding=self.embeddings)
        self.retriever = vector_store.as_retriever(search_type = "mmr", search_kwargs={
            "k": 6,
            "fetch_k": 20,
            "include_metadata": True
            },
        )
        self.retriever_tool = create_retriever_tool(
                self.retriever,
                "uploaded_files_search",
                "Search for information about uploaded files, for any question about uploaded files you should use this tool",
            )
        self.tools.append(self.retriever_tool)
        self.agent = create_openai_functions_agent(self.model, self.tools, self.prompt)



    def ask(self, query: str):
        agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True)
        result = agent_executor.invoke({"input": query})
        return result["output"]


if __name__ == "__main__":
    chat = ChatAI()
    chat.ingest("test.pdf")

    print(chat.ask("What is critical thinking?"))