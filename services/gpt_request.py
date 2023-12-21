
class GPTAPIrequest:
    model_3: str = "gpt-3.5-turbo"
    model_4: str = "gpt-4"
    model_3_16: str = "gpt-3.5-turbo-16k-0613"

    def __init__(self, api_key, system_assistant_prompt, prompt, assistant:Assistant):
        openai.api_key = api_key
        self.system_assistant = system_assistant_prompt
        self.prompt = prompt
        self.assistant = assistant

    def send_request_to_chatgpt(self, messages):
        print(messages)
        response = openai.chat.completions.create(
            model=self.model_4,
            timeout=6000,
            messages=messages,
            n=1,
            stop=None,
            temperature=0.4,
            frequency_penalty=0,
            top_p=0.8,
            presence_penalty=-0,

        )

        response_message = response.dict()['choices'][0]['message']['content'].strip()
        print('ответ от чата: ' + response_message)
        return response_message

    async def hello_message_to_new_other_user(self, to_user_name: str | None):
        if to_user_name:
            prompt_text = [
                {"role": "system",
                 "content":f'{LEXICON_RU["hello_message_to_new_other_user"]} имя написавшего тебе человека: <{to_user_name}>'}]
            return self.send_request_to_chatgpt(prompt_text)
        else:
            prompt_text = [
                {"role": "system",
                 "content": f'{LEXICON_RU["hello_message_to_new_other_user"]}'}]
            return self.send_request_to_chatgpt(prompt_text)

    async def send_first_ping_message(self, to_user_name: str | None):
        if to_user_name:
            prompt_text = [
                {"role": "system", "content": f'{self.assistant.first_ping_message}'}]
            return self.send_request_to_chatgpt(prompt_text)

    async def hello_message(self, to_user_name: str | None):
        if to_user_name:
            prompt_text = [
                {"role": "system", "content": f'{self.assistant.system_assistant_hello_prompt}: <{to_user_name}>'}]
            return self.send_request_to_chatgpt(prompt_text)
        else:
            prompt_text = [
                {"role": "system", "content": f'{self.assistant.system_assistant_hello_prompt}'}]
            return self.send_request_to_chatgpt(prompt_text)

    async def initialize_dialog(self):
        prompt_text = [{"role": "system", "content": self.assistant.system_assistant_prompt}]
        return self.send_request_to_chatgpt(prompt_text)

    async def ask_info(self, user_message):
        prompt_text = [{"role": "system", "content": self.system_assistant},
                       {"role": "user", "content": f'{self.prompt} + "\n", {user_message}'}
                       ]
        return self.send_request_to_chatgpt(prompt_text)