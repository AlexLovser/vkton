from datetime import datetime
from vkton.errors import *
import requests
import os
from PIL import Image


class Object:
	def __getattribute__(self, __name: str):
		if __name != 'last_used':
			self.last_used = datetime.now()
		try:
			return super().__getattribute__(__name)
		except:
			return None


class User(Object):
	def __init__(self, **kwargs):
		self.id = kwargs['user_id']
		self.name = kwargs.get('name', 'Аноним')
		self.tag = f'@id{self.id}({self.name})'
		self.current_page = 'start'
		self.bot = kwargs.get('bot')
		self.last_used = datetime.now()

	@property
	def direct_url(self):
		return f'https://vk.com/id{self.id}'

	@property
	def dialog_url(self):
		return f'https://vk.com/gim{self.bot.group_id}?sel={self.id}'

	def send(self, text, keys: list = None, photo_url: str = None, carousel: list = None):
		self.bot.send(text, user_id=self.id, keys=keys, photo_url=photo_url, carousel=carousel)

	def __repr__(self):
		return f'<User {self.tag}>'


class Message:
	def __init__(self, content: str, author: User, date, message_id, payload=None, attachments=None):
		self.content = content
		self.author = author
		self.user = self.author
		self.date = date
		self.payload = payload
		self.message_id = message_id
		if not attachments:
			attachments = []
		else:
			atts = []

			for i in attachments:
				if i.endswith('type'):
					atts.append(
						Attachment(
							attach_type=attachments[i],
							attach_id=attachments[i.split('_')[0]],
							message=self
						)
					)

			attachments = atts


		self.attachments: list[Attachment] = attachments
	
	def __str__(self) -> str:
		return str(self.content)

	def __repr__(self):
		return f'<Message | {self.author.name}: "{self.content}">'


class Attachment:
	def __init__(self, attach_type, attach_id, message: Message, fp=None):
		self.attach_type = attach_type
		if attach_id:
			self.owner_id, self.attach_id = attach_id.split('_')
		else:
			self.owner_id = None
		self.message = message
		if not fp:
			self.width = None
			self.height = None
		else:
			with Image.open(fp) as img:
				self.width = img.width
				self.height = img.height

		self.fp = fp

	def get_simple_url(self):
		return f'{self.attach_type}{self.owner_id}_{self.attach_id}'
	
	def crop_for_caruseel(self, save_to=None):
		with Image.open(self.fp) as img:
			width, height = img.size
			expected_height = round(8 / 13 * width)
			expected_width = width
			margin_left = 0
			
			if expected_height > height:
				expected_height = height
				expected_width = round(height * 13 / 8)
				margin_left = int((width - expected_width) // 2)

			margin_top = int((height - expected_height) // 2)

			minwidth = 221
			minheight = 136
			maxwidth = 1495
			maxheight = 920

			if minwidth > expected_width or expected_width > maxwidth:
				raise BadImageSizeError('Incorrect image width')
			
			if minheight > expected_height or expected_height > maxheight:
				raise BadImageSizeError('Incorrect image height')
			
			extra_height = expected_height % 8
			margin_top += extra_height // 2
			expected_height -= extra_height

			extra_width = expected_width - (expected_height // 8 * 13)
			margin_left += extra_width // 2
			expected_width -= extra_width
			
			
			if not save_to:
				save_to = f'{self.message.author.bot.base_dir}/src/attachments/{self.owner_id}_{self.attach_id}-cropped.png'

			cropped_image = img.crop((margin_left, margin_top, margin_left + expected_width, margin_top + expected_height))
			cropped_image.save(save_to)

		return Attachment(self.attach_type, None, message=self.message, fp=save_to)

	def download(self, save_to=None):
		if not save_to:
			save_to = f'{self.message.author.bot.base_dir}/src/attachments/{self.owner_id}_{self.attach_id}.png'

		response = requests.get(
			'https://api.vk.com/method/messages.getById', 
			params={
				'access_token': TOKEN, 
				'v': 5.131, 
				'message_ids': [self.message.message_id]
			}
		)

		response = response.json()

		sizes = response['response']['items'][0]['attachments'][0]['photo']['sizes']
		the_greatest = max(sizes, key=lambda x: x['height'])
	
		response = requests.get(the_greatest['url'])

		with open(save_to, 'wb') as f:
			f.write(response.content)


		self.fp = save_to

		return self
		
	def upload(self):
		details = self.message.author.bot.upload_photo(self.fp)
		self.attach_id = details['id']
		self.owner_id = details['owner_id']

		return self

	def delete(self):
		try:
			os.remove(self.fp)
		except:
			pass