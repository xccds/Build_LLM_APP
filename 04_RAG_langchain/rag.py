from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

class ChatDoc:

    def __init__(self):
        self.model = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.embeddings = OpenAIEmbeddings()
        #self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        system_prompt = (
            '''
            You are an assistant for question-answering tasks. 
            Use the following pieces of retrieved context to answer the question. 
            If you don't know the answer, say that you don't know.
            context: {context}'''
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{question}"),
            ]
        )

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
        self.chain = ({"context": self.retriever| format_docs, "question": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())


    def ask(self, query: str):
        if not self.chain:
            return "please add document first"
        response = self.chain.invoke(query)
        return response
    
    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None


if __name__ == "__main__":
    chat = ChatDoc()
    chat.ingest("test.pdf")

    print(chat.ask("What is critical thinking?"))