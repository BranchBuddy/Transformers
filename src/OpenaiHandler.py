import json
import os
import time
import yaml
from dotenv import load_dotenv
from openai import OpenAI

class OpenAiHandler:
    """
    A class that handles interactions with OpenAI's text-davinci-003 model for code summarization.
    """

    def __init__(self, prompts_path='src/configs/prompts.yaml') -> None:
        """
        Initializes the OpenAiHandler class.

        Loads the OpenAI API key from the environment variables and creates an instance of the OpenAI class.
        """
        load_dotenv()
        openai_key = os.getenv("OPENAI_KEY")
        self.client = OpenAI(api_key=openai_key)
        self.task_to_assistant = {}
        with open(prompts_path, 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
        self.task_prompts = prompts

    def createAssistant(self, task):
        assistant = self.client.beta.assistants.create(
            name=f"Code {task}",
            instructions=self.task_prompts[task],
            tools=[{"type": "code_interpreter"}],
            model="gpt-4"
        )
        self.task_to_assistant[task] = assistant.id

    def handleTask(self, task, content):
        # This code is for v1 of the openai package: pypi.org/project/openai
        thread = self.client.beta.threads.create()
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=content
        )
        question_id = message.id
        
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.task_to_assistant[task],
        )
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id= run.id
        )
        start_time = time.time()
        while True:
            messages = self.client.beta.threads.messages.list(
            thread_id=thread.id
            )
            last_message = messages.data[0]
            message_content = last_message.content[0].text.value
            last_id = last_message.id
            if last_id != question_id and message_content != '':
                break
        end_time = time.time()
        time_diff = end_time - start_time
        return {'time': time_diff, 'response': message_content}
    