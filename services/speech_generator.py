import os
from datetime import datetime


from elevenlabs import generate, save, set_api_key
from environs import Env
env: Env = Env()
env.read_env('.env')
set_api_key(env("ELEVEN_API_KEY"))

def text_to_speach_elevenlabs(text, chat_id, message_id):
    audio = generate(
        text=text,
        voice="Chernyshov",
        model="eleven_multilingual_v2"
    )
    current_dir = os.path.dirname(__file__)

    filename = os.path.join(current_dir,'temp_docs','outcome_voices',
                     f'{chat_id}_{message_id}_{datetime.now().strftime("%Y%H%M%S")}.mp3' )
    save(audio, filename=filename)

    return os.path.normpath(filename)


if __name__ == '__main__':
    text_to_speach_elevenlabs(text="Привет",
                              chat_id=123,
                              message_id=123)