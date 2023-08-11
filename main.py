from utils.classes import *
from utils.bot import Bot
from utils.config import *

from cogs.maincog import *


bot = Bot(TOKEN)


# @Commands.command(keywords=['начать', 'обновить'], back_to='start')
# def start(ctx: Context):
# 	ctx.user.send(
# 		'Добро пожаловать в сообщество!',
# 		keys=[
# 			Button('QQ', 'red')
# 		],
# 	)


# @Commands.task(timeout=5)
# def lol():
# 	bot.get_user(494414313).send(
# 		'Добро пожаловать в сообщество!',
# 		keys=[
# 			Button('QQ', 'red')
# 		],
# 	)




bot.run()
