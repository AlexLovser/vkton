import functools
from .objects import User, Message
from .ui import *
import vkton.errors as errors



class Context:
	def __init__(self, user: User, message: Message, event):
		self.user = user
		self.message = message
		self.content = message.content
		self.send = self.user.send
		self.event = event


class Commands:
	funcs = {}
	tasks = {}

	@classmethod
	def command(cls, *, keywords: list[str] = None, back_to: str, admin_only: bool = False):
		def outer_wrapper(func):
			nonlocal keywords
			if cls.funcs.get(func.__name__):
				raise ValueError(f"Вы создали две одинаковые команды с именем '{func.__name__}'!")
			
			if not keywords:
				keywords = [func.__name__]
			else:
				keywords = list(set([func.__name__, *keywords]))
			
			cls.funcs[func.__name__] = {
				'keywords': [x.lower() for x in keywords],
				'func': func,
				'back_to': back_to, # куда вернуться в случае отмены
				'admin_only': admin_only,

			}			

			@functools.wraps(func)
			def wrapper(*args, **kwargs):
				return func(*args, **kwargs)
			
			return wrapper
		
		return outer_wrapper
	
	@classmethod
	def task(cls, *, timeout: int | float):
		def outer_wrapper(func):
			if cls.tasks.get(func.__name__):
				raise ValueError(f"Вы создали два одинаковых task-loop с именем '{func.__name__}'!")
			
			cls.tasks[func.__name__] = {
				'timeout': timeout,
				'func': func,
			}			
			
			@functools.wraps(func)
			def wrapper(*args, **kwargs):
				return func(*args, **kwargs)
			
			return wrapper
		
		return outer_wrapper
	
	@classmethod
	def parse(cls, text):
		for v in cls.funcs.values():
			for word in v['keywords']:
				if text.lower().startswith(word.lower()):
					fname, args = text[:len(word)].strip(), text[len(word):].strip()
					# print(fname, args)

					if args:
						args = args.split()
					
					return fname, args
		else:
			return text, []

	@classmethod
	def execute(cls, ctx: Context):
		if ctx.message.content:
			fname, args = cls.parse(ctx.message.content)

			for v in cls.funcs.values():
				if fname.lower() in v['keywords']:
					# if v['admin_only'] and not ctx.user.is_admin:
					# 	raise errors.LessPermissionsError()

					if v['func'].__code__.co_argcount == 2:
						v['func'](ctx, ' '.join(args))
					else:
						v['func'](ctx, *args)

					ctx.user.current_page = v['func'].__name__
					
					break
				
			else:
				raise errors.UnknownCommandError(fname)
			
	@classmethod
	def go_back(cls, ctx: Context):
		new_func = Commands.funcs[Commands.funcs[ctx.user.current_page]['back_to']]['func']
		cls.redirect(ctx, new_func.__name__)

	@classmethod
	def redirect(cls, ctx: Context, to):
		new_func = Commands.funcs[to]['func']
		ctx.user.current_page = new_func.__name__
		new_func(ctx)
				
				
class Generator:
	def __init__(self, sequence):
		if isinstance(sequence, (list, tuple, set)):
			sequence = (_ for _ in sequence)
		self.sequence = sequence
		self.generated = []
		self.len_generated = 0

	def get(self, start, end=None):
		if end == None:
			end = start + 1
		diff = end - self.len_generated + 1
		if diff > 0:
			for _ in range(diff):
				try:
					self.generated.append(next(self.sequence))
					self.len_generated += 1
				except (StopIteration, StopAsyncIteration):
					break
		
		items = self.generated[start:end]
		return items
	
	def portions(self, amount, cut=False):
		iteration = 0
		if amount == 1:
			raise ValueError()
		while True:
			items = self.get(iteration * amount, (iteration + 1) * amount)
			items_len = len(items)

			if not items_len:
				break
			if items_len < amount and cut:
				break
			yield items
			iteration += 1

	def index_of(self, item):
		return self.generated.index(item)



