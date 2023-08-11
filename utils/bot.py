from vk_api import VkApi, keyboard
from .connect import ConnectionManager
from vk_api.longpoll import VkLongPoll, VkEventType
import threading
from .objects import User, Message
from .classes import *
from .config import *
import utils.errors as errors 
from time import sleep
import datetime
from uuid import uuid4
from re import compile
from requests.exceptions import ReadTimeout
import time
import json
import requests
import traceback
import logging


logging.basicConfig(filename='applogs.log', level=logging.DEBUG, format='[%(asctime)s] %(levelname)s\nFILE=%(name)s/ MESSAGE="%(message)s"\n')

text_cleaner = compile(r'^[A-zА-я0-9_\\\.+-\[\]\(\)@]')
photo_id_extracter = compile(r'photo-?[0-9]+_[0-9]+')


class MyLongPool(VkLongPoll):
	def listen(bot):
		while True:
			try:
				for event in bot.check():
					yield event
			except ReadTimeout:
				time.sleep(60)
			except Exception as err:
				print('[ ERR ]', err)
				sleep(3)


class Bot:
	vk_session = None
	longpool = None
	events = {}
	sub_events = {}
	user_cache: dict[str, User] = {}
 
	def __init__(self, token, *, cache_refresh_timeout=300):
		self.token = token
		self.vk_session = VkApi(token=token)
		self.longpoll = MyLongPool(self.vk_session)
		self.db = ConnectionManager()
		self.back_button = Button('Назад', 'red')

		
		
		logging.info('The bot is online')

	def clean_text(self, string: str) -> str:
		return string
		# return text_cleaner.sub('', string)

	def wait_message(self, user: User | list[User], *, timeout: int = None, check = None, ignore_backs: bool = False) -> Message | None:
		if timeout is None:
			timeout = 600

		if isinstance(user, User):
			user = [user]

		if check is None:
			def check(message: Message) -> tuple[bool, str | None]:
				return True
			
		def default_check(message):
			text = message.content

			if not text and not message.attachments:
				return False
			else:
				return True
			
		def total_check(message: Message):
			succeed = default_check(message)

			if succeed:
				succeed = check(message)
			
			return succeed

		generated_id = uuid4() # уникальный хеш ивента
		messages: dict[int, Message | None] = {u.id: None for u in user} # данные о сообщениях одного или нескольких юзеров
		global_event = threading.Event() # глобальный ивент

		for u in user:
			self.sub_events[u.id] = generated_id

		self.events[generated_id] = {
			'event': global_event,
			'messages': messages,
			'ignore_backs': ignore_backs,
			'check': total_check
		}

		global_event.wait(timeout) # ожидание глобального события

		
		del self.events[generated_id] # очистка общего вейтера

		for u in user: # очистка суб вейтеров
			try:
				del self.sub_events[u.id]
			except KeyError:
				pass

		if not ignore_backs:
			for message in messages.values():
				if message and message.content.lower() in CANCEL_WORDS:
					raise errors.CancelError(user)
					

		if any(m == None for m in messages.values()):
			for u, m in messages.items():
				author = self.get_user(u)
				if m is None:
					author.send('Вы слишком долго отправляли сообщение! Бот устал ждать...')

				local_context = Context(author, m)
				Commands.go_back(local_context)

			raise errors.TimeoutResponseError()
			
		if len(messages) == 1:
			return messages[list(messages)[0]]
		else:
			return messages # user_id: <Message>

	def _create_keyboard(self, keys):
		if keys is None:
			keys = []

		inline = False
		for button in keys:
			if not isinstance(button, list):
				button = [button]
			if any(i.inline for i in button):
				inline = True
				break

		key = keyboard.VkKeyboard(inline=inline)	

		slots = []

		for k in keys:
			if isinstance(k, list):
				slots.append(k)
				slots.append([])
			
			elif not slots or len(slots[-1]) == 5:
				slots.append([k])
			elif len(slots[-1]) < 5:
				slots[-1].append(k)

		slots = list(filter(None, slots))
				
		row = 0
		for slot in slots:
			for button in slot:
				if button.link:
					key.add_openlink_button(
						label=button.title,
						# color=button.color,
						link=button.link,
						payload=json.dumps(button.payload) if button.payload else None
					)
				else:
					key.add_button(
						label=button.title,
						color=button.color,
						payload=json.dumps(button.payload) if button.payload else None
					)
			if row + 1 != len(slots):
				key.add_line()

			row += 1

		return key

	def _create_carousel(self, fields):
		if fields is None:
			fields = []

		fields = [
			i.body if isinstance(i, CarouselField) else i
			for i in fields
		]

		for i in fields:

			if i.get('photo_id'):
				i['photo_id'] = self.photo_id_from_url(i['photo_id']).replace('photo', '')
			if i.get('buttons'):
				i['buttons'] = [i[0] for i in self._create_keyboard(i['buttons']).keyboard['buttons']]
				for x in i['buttons']:
					x['action']["payload"] = json.dumps(x['action']["payload"])

		body = {
			'type': 'carousel',
			'elements': fields
		}

		return body
	
	def photo_id_from_url(self, url):
		return photo_id_extracter.search(url).group(0)

	def send(self, text, /, user_id, keys: list[Button] = None, photo_url: str = None, carousel=None):
		if not isinstance(user_id, list):
			user_id = [user_id]

		if not user_id:
			return
		
		if len(user_id) > 10:
			for portion in Generator(user_id).portions(2):
				self.send(text, user_id=portion, keys=keys, photo_url=photo_url, carousel=carousel)
				sleep(5)

			return

		key = self._create_keyboard(keys)
		carousel = self._create_carousel(carousel)

		request =  {
			'peer_ids': user_id, 
			'message' : text, 
			'random_id' : 0
		}

		if isinstance(keys, list) and not keys[0]:
			request['keyboard'] = key.get_empty_keyboard(), 
		elif key.keyboard['buttons'][0]:
			request['keyboard'] = key.get_keyboard(), 
		
		if carousel['elements']:
			request['template'] = json.dumps(carousel)

		if photo_url:
			request['attachment'] = photo_url
	

		self.vk_session.method('messages.send', request)

	def get_profile(self, user_id):
		array = self.vk_session.method("users.get", {"user_ids": user_id})
		if array:
			return array[0]
		else:
			return None
	
	def get_user(self, user_id: int):			
		from_cache = self.user_cache.get(user_id)
		if from_cache:
			from_cache.last_used = datetime.datetime.now()
			return from_cache
		
		profile = self.get_profile(user_id)

		if not profile:
			return None

		user = User(
			user_id=user_id,
			name=profile.get('first_name', '?') + ' ' + profile.get('last_name', '?'),
			bot=self
		)

		self.user_cache[user.id] = user

		return user

	def parse_tag(self, string):
		try:
			id_tag, _ = string[1:-1].split('|')
			return int(id_tag[2:])
		except:
			return None

	def _get_upload_server(self):
		response = requests.get(
		'https://api.vk.com/method/photos.getMessagesUploadServer',
			params={
				'access_token': self.token,
				'v': '5.131',
			}
		)

		if response.status_code == 200:
			return response.json()['response']['upload_url']
		else:
			return None
		
	def _upload_photo(self, upload_url, photo):
		response = requests.post(
			upload_url, 
			files={'photo': photo}
		)

		if response.status_code == 200:
			return response.json()
		else:
			return None

	def _save_photo(self, uploaded_data):
		response = requests.get(
			'https://api.vk.com/method/photos.saveMessagesPhoto',
			params={
				'access_token': TOKEN,
				'v': '5.131',
				'server': uploaded_data['server'],
				'photo': uploaded_data['photo'],
				'hash': uploaded_data['hash']
			}
		)

		if response.status_code == 200:
			return response.json()['response'][0]
		else:
			return None

	def upload_photo(self, fp):
		upload_url = self._get_upload_server()

		if not upload_url:
			raise errors.PhotoUploadHasFailedError()

		with open(fp, 'rb') as photo:
			uploaded_data = self._upload_photo(upload_url, photo)
			
			photo_data = self._save_photo(uploaded_data)


		return photo_data

	def run(self,):
		def cache_clearing_task():
			new_cache = {}

			for k, v in self.user_cache.items():
				if (datetime.datetime.now() - v.last_used).total_seconds() < 600:
					new_cache[k] = v

			self.user_cache = new_cache

		Commands.tasks['cache_clearing_task'] = {
			'timeout': 600,
			'func': cache_clearing_task
		}

		for name, task in Commands.tasks.items():
			logging.info(f'{name}, {task}')

			def task_delay_wrapper(timeout, f):
				while True:
					f()
					sleep(timeout)

			threading.Thread(name=name, target=task_delay_wrapper, args=(task['timeout'], task['func'])).start()

		for event in self.longpoll.listen(): # слушатель ивентов
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				if ALLOWED_USERS == '__all__' or event.user_id in ALLOWED_USERS:
					def do(e):
						user_id = e.user_id
						payload = event.extra_values.get('payload', 'None')
						try:
							payload = eval(payload.strip('"').replace('\\"', '"'))
						except:
							payload = {}

						attachments = event.attachments
						message_id = event.message_id
						user = self.get_user(user_id)
						message = Message(
							self.clean_text(e.text), 
							user, 
							datetime.datetime.now(), 
							message_id=message_id,
							payload=payload, 
							attachments=attachments
						)
						context = Context(user, message) # создание контекста, информация о команде
						sub_waiter_event = self.sub_events.get(user.id)
						main_waiter_event = self.events.get(sub_waiter_event)
						is_back_command = message.content.lower() in CANCEL_WORDS

						try:
							if main_waiter_event:
								ignore_backs = main_waiter_event['ignore_backs']
								if is_back_command and ignore_backs: # если чел написал назад но включен игнор
									user.send('В данный момент невозможно вернуться назад...')
								else:
									succeed = main_waiter_event['check'](message)
									
									if succeed:
										del self.sub_events[user.id]
										messages = main_waiter_event['messages']
										messages[user.id] = message

										if all(messages.values()) or (is_back_command and not ignore_backs):
											main_waiter_event['event'].set()
								
							elif is_back_command:
								raise errors.CancelError([user])
							else:
								Commands.execute(context)

						except errors.TimeoutResponseError:
							return 

						except errors.CancelError as err:
							for u in err.args[0]:
								local_context = Context(u, message)
								Commands.go_back(local_context)

							return 

						except errors.LessPermissionsError as err:
							return user.send('У вас недостаточно прав для использования этой команды')

						except errors.UnknownCommandError as err:
							return
							# return print(f'Команда {err.args[0]} не найдена!')
						
						except Exception as err:
							print(traceback.print_exc())
						
							try:
								Commands.redirect(context, 'start') # у случае хз каких ошибок вернуться в главное меню
							except:
								pass

						finally:
							pass
			

							
					threading.Thread(name=f'Command "{event.text}"', target=do, args=(event, )).start()

