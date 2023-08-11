<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="VK-Ton" />

  &#xa0;

  <!-- <a href="https://vkton.netlify.app">Demo</a> -->
</div>

<h1 align="center">VK-Ton</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/AlexLovser/VK-ton?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/AlexLovser/VK-ton?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/AlexLovser/VK-ton?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/AlexLovser/VK-ton?color=56BEB8">

  <img alt="Github issues" src="https://img.shields.io/github/issues/AlexLovser/VK-ton?color=56BEB8" />

  <img alt="Github forks" src="https://img.shields.io/github/forks/AlexLovser/VK-ton?color=56BEB8" />

  <img alt="Github stars" src="https://img.shields.io/github/stars/AlexLovser/VK-ton?color=56BEB8" />
</p>

<!-- Status -->

<!-- <h4 align="center"> 
	🚧  VK Ton 🚀 Under construction...  🚧
</h4> 

<hr> -->

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <!-- <a href="#memo-license">License</a> &#xa0; | &#xa0; -->
  <a href="https://github.com/AlexLovser" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

`vk-ton` это модуль для упрощенного создания VK ботов на Python. В библиотеке вы найдете все необходимые классы, для ванильного использования vk-api.

## :sparkles: Features ##

:heavy_check_mark: Удобное и быстрое создание цепочек команд;\
:heavy_check_mark: Возможность разделять код в несколько файлов;\
:heavy_check_mark: Все необходимые функции для быстрого старта;

## :rocket: Technologies ##

Технологии использованные в проекте:

- [Python3](https://python.org/)
- [VK-API](https://dev.vk.com/ru/reference)


## :checkered_flag: Starting ##

```bash
# Установка самого модуля
$ pip install vkton

# Проверка, что все зависимости установлены
$ pip install PIL vk-api

```

Мой модуль гибко решает проблему навигации в боте. В каждом декораторе команды обязательным является параметр `back_to`. В него следует вписать название функции, которая будет вызвана в случае попытки пользователем выйти назад. Это позволяет не задумываясь сделать вложенные меню.
Если вы описываете корневое меню, то впишите в `back_to` ее же название.

```py
from vkton import Bot, Commands, Context
from vkton.ui import Button


# Команду можно вызвать по любому слову из **keywords** или по названию функции (hello, meteo ...)
@Commands.command(keywords=["Поздароваться", 'Say hello'], back_to='hello')
def hello(ctx: Context):
    ctx.user.send(
        'Hello, my Friend! You are using VK-ton by Alex Lovser! Nice to see you!',
        keys=[
          Button('Погода', 'white'), # В данный кнопках по умолчанию параметр inline=False
          Button('Кнопка с ссылкой', 'red', link='https://pornhub.com')
        ]
    )


# Если будет написана фраза "Назад", то будет вызвана функция hello
@Commands.command(keywords=['Погода'], back_to='hello') 
def meteo(ctx: Context):
    ctx.user.send(
        'Погода обещает быть замечательной',
        keys=[
          bot.back_button # Заготовленная красаня кнопка "Назад"
        ]
    )

```
К слову вы можете удобно настроить ряды кнопок с помощью списков

```py
... # Если вы хотите сгруппировать кнопки на одном ряду, то просто оберните их в список
keys=[
  [
    Button('Первая', 'white'), 
    Button('Вторая', 'white'),
  ],
  Button('Третья', 'white'),

]
...
```
### __Каждая кнопка принимает несколько параметров:__\
**Обязательные** *<Позиционные>*\
`:title:` - Текст на кнопке\
`:color:` - 'red', 'green', 'blue', 'white' или те же слова на русском языке. Цвет самой кнопки.

**Необязательные** *<Именные>*\
`:link:` - Используется для создания кнопки-ссылки\
`:inline:` - Если в сообщении хотябы одна кнопка имеет данный параметр *True*, то кнопки появляются не в клавиатуре, а под сообщением.\
`:payload:` - Словарь с контекстными данными для команды. После нажатия кнопки в объекте `ctx.message.payload` можно будет увидеть эти данные



## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


С :heart: от <a href="https://github.com/AlexLovser" target="_blank">Alex Lovser</a>

&#xa0;

<a href="#top">Вернуться вверх</a>
