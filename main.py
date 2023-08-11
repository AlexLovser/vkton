from utils.classes import *
from utils.bot import Bot
from utils.config import *
from utils.ui import CarouselField

from cogs.maincog import *


bot = Bot(TOKEN)


bot.wait_message()
@Commands.task(timeout=3600) # время в секундах
def c(ctx: Context):
	bot.get_user(12345678).send(
		'Hello, world!',
        carousel=[
            CarouselField(
		        photo_id='photo12345678_12345678',
                title='TITLE1',
                description='description1',
                buttons=[
                    Button('Подробнее', 'blue', payload={'some_id': '12345'})
                ]
		    ),
		    CarouselField(
		        photo_id='photo12345678_12345678',
                title='TITLE2',
                description='description2',
                buttons=[
                    Button('Подробнее', 'blue', payload={'some_id': '67890'})
                ]
		    ),
		    
        ]
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
