import os
import logging

class Interview:

    def __init__(self):
        self.package_directory = os.path.dirname(__file__)

        with open(self.package_directory + "/prompt.txt", 'r', encoding='utf-8') as file:
            self.__system_prompt_template = file.read()

    def get_prompts_for_session(self):
        prompts = [self.__system_prompt_template]
        return prompts
