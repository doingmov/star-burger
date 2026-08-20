# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)

Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Как запустить dev-версию сайта

Для запуска сайта нужно запустить **одновременно** бэкенд и фронтенд, в двух терминалах.

### Как собрать бэкенд

Скачайте код:

```sh
git clone https://github.com/devmanorg/star-burger.git
```

Перейдите в каталог проекта:

```sh
cd star-burger
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен:

```sh
python --version
```

**Важно!** Версия Python должна быть не ниже 3.10.

Создайте виртуальное окружение:

```sh
python -m venv venv
```

Активируйте его:

- Windows:

```sh
.\venv\Scripts\activate
```

- MacOS/Linux:

```sh
source venv/bin/activate
```

Установите зависимости:

```sh
pip install -r requirements.txt
```

### Настройка переменных окружения

Создайте файл `.env` в корне проекта, рядом с `manage.py`.

Пример:

```env
SECRET_KEY=your-secret-key
YANDEX_GEOCODER_API_KEY=your-yandex-geocoder-api-key
DATABASE_URL=postgres://star_burger_user:your-password@localhost:5432/star_burger
```

Для локальной разработки используется PostgreSQL, поэтому перед запуском проекта необходимо установить PostgreSQL и создать базу данных и пользователя.

### Настройка PostgreSQL

Создайте пользователя и базу данных PostgreSQL:

```sql
CREATE USER star_burger_user WITH PASSWORD 'your-password';
CREATE DATABASE star_burger OWNER star_burger_user;
```

Не используйте пароль из примера в реальном проекте. Пароль должен храниться только в `.env`.

После создания базы данных выполните миграции:

```sh
python manage.py migrate
```

Если необходимо перенести данные из старой SQLite-базы, сначала создайте дамп:

```sh
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > dump.json
```

Затем выполните миграции PostgreSQL:

```sh
python manage.py migrate
```

И загрузите данные:

```sh
python manage.py loaddata dump.json
```

Проверьте подключение к PostgreSQL:

```sh
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['ENGINE']); print(settings.DATABASES['default']['NAME'])"
```

В результате должно быть примерно:

```text
django.db.backends.postgresql
star_burger
```

### Запуск сервера

```sh
python manage.py runserver
```

Откройте сайт в браузере:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Если вы увидели пустую белую страницу, не пугайтесь — возможно, ещё не собран фронтенд.

## Как собрать фронтенд

**Откройте новый терминал.** Для работы сайта в dev-режиме одновременно должны работать `runserver` и `parcel`.

[Установите Node.js](https://nodejs.org/en/), если его ещё нет.

Проверьте версии:

```sh
node --version
npm --version
```

Перейдите в каталог проекта и установите пакеты:

```sh
cd star-burger
npm ci --dev
```

Запустите Parcel:

Linux/MacOS:

```sh
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Windows:

```sh
.\node_modules\.bin\parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Дождитесь завершения первичной сборки. О готовности можно узнать по сообщению вида:

```text
✨ Built in 10.89s
```

После этого обновите страницу сайта.

**Если сайт отображается некорректно, сбросьте кэш браузера сочетанием `Ctrl-F5`.**

## Как запустить prod-версию сайта

Сначала установите зависимости Python и Node.js, как описано выше.

Соберите фронтенд:

```sh
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
```

На Windows:

```sh
.\node_modules\.bin\parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
```

### Настройка production

Создайте файл `.env` в корне проекта, рядом с `manage.py`.

Пример:

```env
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain-or-ip
YANDEX_GEOCODER_API_KEY=your-yandex-geocoder-api-key
DATABASE_URL=postgres://star_burger_user:your-password@localhost:5432/star_burger
```

`SECRET_KEY`, пароль PostgreSQL и другие секретные данные нельзя хранить в репозитории.

После настройки базы данных выполните:

```sh
python manage.py migrate
python manage.py collectstatic
```

Запустить production-сервер можно, например, через Gunicorn:

```sh
gunicorn star_burger.wsgi:application
```

В production рекомендуется запускать приложение через systemd и проксировать его через Nginx.

## Перенос данных с SQLite на PostgreSQL

Если проект ранее использовал SQLite, данные можно перенести с помощью стандартных команд Django.

На старой базе создайте дамп:

```sh
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > dump.json
```

После переключения проекта на PostgreSQL создайте структуру базы:

```sh
python manage.py migrate
```

Затем загрузите данные:

```sh
python manage.py loaddata dump.json
```

После переноса можно проверить количество объектов, например:

```sh
python manage.py shell -c "from foodcartapp.models import Restaurant, Product; print('Restaurants:', Restaurant.objects.count()); print('Products:', Product.objects.count())"
```

SQLite-файл `db.sqlite3` после успешного переноса больше не используется.

## Проверка проекта

Проверить настройки Django:

```sh
python manage.py check
```

Проверить состояние миграций:

```sh
python manage.py showmigrations
```

Проверить, что используется PostgreSQL:

```sh
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['ENGINE'])"
```

Ожидаемый результат:

```text
django.db.backends.postgresql
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:

- Второй и третий урок [учебного курса Django](https://dvmn.org/modules/django/).
