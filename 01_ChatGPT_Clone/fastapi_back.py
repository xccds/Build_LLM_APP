from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
app = FastAPI()


class Item(BaseModel):
    role: str
    content: str

class ReqestIntputs(BaseModel):
    model: str
    messages: list[Item]

def openai_response(model,messages):
    chat_response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    reply = chat_response.choices[0].message.content
    return reply

@app.post("/openai")
async  def openai_AI(reqest_intputs:ReqestIntputs):
    reply = openai_response(reqest_intputs.model, reqest_intputs.messages)
    return reply

