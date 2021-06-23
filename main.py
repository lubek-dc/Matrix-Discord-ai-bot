import os

import discord
import pyttsx3
import requests
import speech_recognition as sr
from discord.ext import commands
from configparser import ConfigParser

WIT_API_HOST = os.getenv('WIT_URL', 'https://api.wit.ai')
WIT_API_VERSION = os.getenv('WIT_API_VERSION', '20200513')
config = ConfigParser()
config.read('./config.ini')
TOKEN_PL = config.get('Wit', 'PL')  # for secure (hidden token)
TOKEN_EN = config.get('Wit', 'EN') # for secure (hidden token)
DISCORD_TOKEN = config.get('Discord', 'TOKEN')
jezyk = "pl"
client = commands.Bot(command_prefix='?')


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        command = str(message.content)
        if message.content.startswith('!!!'):
            command = command.replace("!!!", "")
            bot = Repeat(command, message, False, 'EN')
            await message.reply(bot, mention_author=False)
            print(str(message.author) + ': ' + str(command))
            print('response: ' + bot)
        elif message.content.startswith('!!'):
            command = command.replace("!!", "")
            bot = Repeat(command, message, False, 'PL')
            await message.reply(bot, mention_author=False)
            print(str(message.author) + ': ' + str(command))
            print('response: ' + bot)


try:
    engine = pyttsx3.init()
except ImportError:
    print("Requested Driver not found")
except RuntimeError:
    print('Driver fails to initialise')

voices = engine.getProperty('voices')
for voice in voices:
    print(voice.id)
if jezyk == 'pl':
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PL-PL_PAULINA_11.0')
elif jezyk == 'eng':
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate)


def Repeat(text, user, debug, Language):
    if Language == 'PL':
        data = text_ai(text, Language)
        try:
            print(str(user.author) + ' : {}'.format(data['text']))
            if not debug:
                response = data['response']
                if response:
                    return response
            if debug:
                texter = data['text']
                confidence = data['confidence']
                response4response = data['response']
                response = f'Text: {texter}, Confidence: {confidence}, Response:{response4response}'
                if response:
                    return response

        except Exception as e:
            return text
    elif Language == 'EN':
        data = text_ai(text, Language)
        try:
            print(str(user.author) + ' : {}'.format(data['text']))
            if not debug:
                response = data['response']
                if response:
                    return response
            if debug:
                texter = data['text']
                confidence = data['confidence']
                response4response = data['response']
                response = f'Text: {texter}, Confidence: {confidence}, Response:{response4response}'
                if response:
                    return response

        except Exception as e:
            return 'nie rozumiem'


def open():
    print("open")
    # playsound('open.wav')


def close():
    print("close")
    # playsound('close.wav')


def text_ai(text, language):
    if language == 'PL':
        try:
            full_url = "https://api.wit.ai/message?v=20210530&q={}".format(text)
            headers = {
                'authorization': 'Bearer ' + TOKEN_PL,
                'accept': 'application/vnd.wit.' + WIT_API_VERSION + '+json'
            }
            rsp = requests.request('GET', full_url, headers=headers).json()
            # print(rsp)
            response = rsp['traits']['Response'][0]['value']
            text = rsp['text']
            intent = rsp['intents'][0]["name"]
            confidence = rsp['intents'][0]["confidence"]
            entity = rsp['entities']
            data = {
                'text': text,
                'intent': intent,
                'entity': entity,
                'confidence': confidence,
                'response': response,
            }
            return data
        except:
            return 'Nie rozumiem'
            print('cmd: ' + text + ' (idk)')
            value = True
            Repeat(value)
    if language == 'EN':
        try:
            full_url = "https://api.wit.ai/message?v=20210530&q={}".format(text)
            headers = {
                'authorization': 'Bearer ' + TOKEN_EN,
                'accept': 'application/vnd.wit.' + WIT_API_VERSION + '+json'
            }
            rsp = requests.request('GET', full_url, headers=headers).json()
            # print(rsp)
            response = rsp['traits']['Response'][0]['value']
            text = rsp['text']
            intent = rsp['intents'][0]["name"]
            confidence = rsp['intents'][0]["confidence"]
            entity = rsp['entities']
            data = {
                'text': text,
                'intent': intent,
                'entity': entity,
                'confidence': confidence,
                'response': response,
            }
            return data
        except:
            return "I don't know"
            value = True
            Repeat(value)


if __name__ == '__main__':
    client = MyClient()
    client.run(DISCORD_TOKEN)
