# Оглавление

1. [Задание](#Задание)
1. [Результаты](#Результаты)
2. [Build](#Build)

# Задание

## Задача 1
Необходимо разработать сервис построения ортодромии. 

Серверная географическая задача: функция формирования ортодромии.

Входные параметры: Координаты точки начала, координаты точка конца, количество узлов.

На выходе — полилиния.

Фронтэнд: форма ввода параметров (2 точки, кол-во узлов), отправка запроса на сервер, получение ответа,и отображение линии на карте.

## Задача 2
Сервис высот (elevation service)

Необходимо разработать веб-сервер с одной (пока что функцией):

по запросу типа http://[ip-адрес]:[порт]/elevation?wkt={wkt} возвращать ту же геометрию в формате wkt, но с данными о высоте.

# Результаты

![use_case](img/use_case.gif)

# Build

## Quickstart

1. Requires installation of Flask, geomet, pyproj, rasterio etc

```bash
pip install -r requirements.txt
```

2. Run 

```bash
flask run 
```

3. Open url

```
127.0.0.1:5000
```

## Docker

1. Build docker container

```bash
docker image build -t python-flask-docker .  
```

2. Run docker container

```bash
docker container run -p 5001:5000 python-flask-docker
```

3. Open url

```
127.0.0.1:5001
```

