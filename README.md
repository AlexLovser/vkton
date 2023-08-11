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

```py
from vkton import Bot, Commands, Context

@Commands.command(keywords=["Поздароваться", 'Say hello'])
def hello(ctx: Context):
    ctx.user.send(
        'Hello, my Friend! You are using VK-ton by Alex Lovser! Nice to see you!'
    )

```


## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


С :heart: от <a href="https://github.com/AlexLovser" target="_blank">{{Alex Lovser}}</a>

&#xa0;

<a href="#top">Вернуться вверх</a>
