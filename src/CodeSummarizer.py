import time
import requests
from openai import OpenAI
class CodeSummarizer:

    def __init__(self):
        self.opanai_key = "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"
        self.client = OpenAI(api_key=self.opanai_key)
        self.createSummaryAssistant()
    
    def createSummaryAssistant(self):
        assistant = self.client.beta.assistants.create(
            name="Math Tutor",
            instructions="You are a code summarizer that for a snippet of codes returns the set of the most important features provided by the code",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview"
        )
        self.summaryAssistant = assistant

    def summarizeCode(self, code: str):
        # This code is for v1 of the openai package: pypi.org/project/openai
        thread = self.client.beta.threads.create()
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=code
        )
        
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.summaryAssistant.id,
        )

        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        time.sleep(50)
        
        messages = self.client.beta.threads.messages.list(
        thread_id=thread.id
        )
        response = messages.last_id
        print(response)
        message = self.client.beta.threads.messages.retrieve(
            thread_id=thread.id,
            message_id=response
            )

        # Extract the message content
        message_content = message.content[0].text

        print(f'MESSAGES#####: {message_content}')
