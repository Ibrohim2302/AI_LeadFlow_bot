# Telegram AI Sales Bot / Telegram AI бот для продаж

Production-ready Telegram bot template built with `aiogram`, `SQLite`, and `OpenAI`.

Готовый шаблон Telegram-бота для бизнеса на `aiogram`, `SQLite` и `OpenAI`.

Python requirement / Требование к Python: `3.10+`

## Features / Возможности

- AI chat with OpenAI in a professional sales tone
- Lead generation with name, phone, request, and admin notifications
- Service menu, order flow, contact flow, FAQ, and message history
- SQLite database with `users`, `messages`, and `leads`
- Anti-spam middleware
- Russian and English interface
- Logging and basic error handling

## Project structure / Структура проекта

```text
.
├── app
│   ├── handlers
│   ├── middlewares
│   ├── services
│   ├── config.py
│   ├── database.py
│   ├── keyboards.py
│   ├── states.py
│   ├── texts.py
│   └── utils.py
├── .env.example
├── main.py
└── requirements.txt
```

## Installation / Установка

1. Create a virtual environment / Создайте виртуальное окружение:

```bash
python -m venv .venv
```

2. Activate it / Активируйте его:

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

3. Install dependencies / Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and fill in your data.

4. Скопируйте `.env.example` в `.env` и заполните своими данными.

5. Run the bot / Запустите бота:

```bash
python main.py
```

## Required settings / Обязательные настройки

In `.env`:

- `BOT_TOKEN` - token from `@BotFather`
- `OPENAI_API_KEY` - your OpenAI API key
- `ADMIN_ID` - Telegram user ID of the admin
- `OPENAI_MODEL` - OpenAI model name
- `SALES_USERNAME` - your Telegram username for sales
- `PRICE_FROM` - starting price for the offer
- `DELIVERY_TIME_RU` / `DELIVERY_TIME_EN` - delivery time for RU/EN texts

В `.env`:

- `BOT_TOKEN` - токен от `@BotFather`
- `OPENAI_API_KEY` - ваш OpenAI API ключ
- `ADMIN_ID` - Telegram ID администратора
- `OPENAI_MODEL` - модель OpenAI
- `SALES_USERNAME` - ваш Telegram username для связи
- `PRICE_FROM` - стартовая цена оффера
- `DELIVERY_TIME_RU` / `DELIVERY_TIME_EN` - срок выполнения для RU/EN

## Customization / Кастомизация

- Edit business information in `.env`
- Edit offer price, delivery time, and Telegram contact in `.env`
- Edit services in `app/config.py` inside `default_services()`
- Edit FAQ answers in `app/config.py` inside `default_faqs()`
- Change sales tone in `app/services/ai_service.py`

- Изменяйте информацию о бизнесе в `.env`
- Изменяйте цену оффера, срок и Telegram-контакт в `.env`
- Изменяйте услуги в `app/config.py` в `default_services()`
- Изменяйте FAQ в `app/config.py` в `default_faqs()`
- Меняйте стиль продаж в `app/services/ai_service.py`

## Notes / Примечания

- The bot uses long polling, which is perfect for MVP and many client projects.
- For high-load production you can move it to webhooks later.
- All leads are stored in SQLite and also sent to the admin chat.

- Бот использует long polling, этого достаточно для MVP и многих клиентских проектов.
- Для высокой нагрузки позже можно перейти на webhooks.
- Все заявки хранятся в SQLite и отправляются администратору.
