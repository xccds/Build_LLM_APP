from openai import OpenAI
import ollama

standards = """
you are a best writer assistant.
you follow 3 key standards that make your writing clear, concise, and engaging.
Clarity means Simple Language, Logical Structure, Focus.
Conciseness means Brevity, Directness, Efficiency.
Engagement means Vivid Language, Active Voice, Varied Sentence Structure.
you can write in english and chinese.
"""

class WriterAssistant:
    def __init__(self,model='gpt-3.5-turbo'):
        self.messages = [{"role": "system", "content": standards}]
        self.client = OpenAI()
        self.model = model
        self.reply = None

    def set_model(self,model):
        self.model = model

    def clear_messages(self):
        self.messages = [{"role": "system", "content": standards}]

    def openai_response(self):
        chat_response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        self.reply = chat_response.choices[0].message.content

    def ollama_response(self):
        chat_response = ollama.chat(model=self.model, 
                        messages=self.messages)
        self.reply = chat_response['message']['content']


    def call_LLM(self):
        if self.model =='llama3':
            self.ollama_response()
        else:
            self.openai_response()


    def improve_write(self,text):
        self.clear_messages()
        prompt = f"Please improve the following text: {text}, output should in chinese and english."
        self.messages.append({"role": "user", "content": prompt})
        self.call_LLM()

    def fix_grammar(self,text):
        self.clear_messages()
        prompt = f"Please fix the grammar in the following text: {text}, output should include correct text and explain the error. output should in chinese and english."
        self.messages.append({"role": "user", "content": prompt})
        self.call_LLM()

    def new_article(self,text):
        self.clear_messages()
        prompt = f"Please write a new article based on the following topic: {text}, output should in chinese and english."
        self.messages.append({"role": "user", "content": prompt})
        self.call_LLM()

    def get_reply(self):
        return self.reply

if __name__ == "__main__":
    gpt = WriterAssistant()
    gpt.new_article("life and journey")
    reply = gpt.get_reply()
    print(reply)