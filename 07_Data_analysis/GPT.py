from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import pandas as pd
import json


class DataAI:

    def __init__(self,data):
        self.df = data
        self.parser = StrOutputParser()
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        self.agent = create_pandas_dataframe_agent(self.llm, self.df, agent_type="openai-tools", verbose=True,allow_dangerous_code=True)

    def create_questions(self):
        prompt = """you are a data scientist. you should create a data analysis report to get insights based on the data information provided. 
            step 1: think and write some questions for this data analysis report.
            step 2: Structure the output information as a JSON as follows.
            Example:
            {"output": [
            "question 1 for report",
            "question 2 for report",
            "question 3 for report",
            ]}
            Your answer should only contain the JSON - no markdown formatting.
            """
        questions = self.agent.invoke({"input": prompt})
        self.questions = json.loads(questions['output'])['output']

    def ask_question(self,question):
        return self.agent.invoke({"input": question})

    def answer_questions(self):
        self.answers = []
        for question in self.questions:
            self.answers.append(self.ask_question(question))
        self.analysis_result = json.dumps(self.answers)

    def create_report(self):
        prompt_template = PromptTemplate.from_template("you are a data scientist, you should create a data analysis report to get insights based on the data analysis_result below: ({analysis_result}).")
        chain = prompt_template | self.llm | self.parser
        self.report = chain.invoke({"analysis_result": self.analysis_result})


if __name__ == "__main__":
    data = pd.read_excel("Titanic.xlsx")
    dataAI = DataAI(data)
    print(dataAI.ask_question("What is the survival rate?"))
    # Is there a notable difference in survival based on the sex?
    # dataAI.create_questions()
    # dataAI.answer_questions()
    # dataAI.create_report()
    # print(dataAI.report)