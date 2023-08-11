from vk_api import keyboard


class Button:
	def __init__(self, title: str, color: str, inline: bool = False, link: str = None, payload=None):
		self.color = {
			'зеленый' : 'positive', 
			'green' : 'positive', 
			'красный' : 'negative', 
			'red' : 'negative', 
			'синий' : 'primary', 
			'blue' : 'primary', 
			'белый' : 'secondary',
			'white' : 'secondary'
		}.get(color.lower(), color)

		self.color = getattr(keyboard.VkKeyboardColor, self.color.upper())
		self.title = title
		self.inline = inline
		self.link = link
		self.payload = payload

	def __str__(self) -> str:
		return f'<Button "{self.title}" color="{self.color}">'


class CarouselField:
	def __init__(self, photo_id, title=None, description=None, action = None, buttons=None, ):
		self.photo_id = photo_id
		self.action = action
		self.title = title
		self.description = description
		self.buttons = buttons if buttons is not None else []

		if not all((title, description)) and any((title, description)):
			raise ValueError('Title and not description')
	
	@property
	def body(self):
		body = {
			"title": self.title,
			"photo_id": self.photo_id,
		}

		if self.action:
			body['action'] = self.action
		
		if self.description:
			body['description'] = self.description

		if self.buttons:
			body['buttons'] = self.buttons

		return body

