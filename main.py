from utils.classes import *
from utils.bot import Bot
from utils.config import *

from cogs.maincog import *


bot = Bot(TOKEN)


@Commands.task(timeout=3600) # время в секундах
def say_hello_task(ctx: Context):
	bot.get_user(12345678).send(
		'Hello, world!',
		attachments='photo12345678_12345678'
		
    )



# @Commands.task(timeout=5)
# def lol():
# 	bot.get_user(494414313).send(
# 		'Добро пожаловать в сообщество!',
# 		keys=[
# 			Button('QQ', 'red')
# 		],
# 	)




bot.run()
