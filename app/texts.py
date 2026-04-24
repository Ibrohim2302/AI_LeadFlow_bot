"""Localized static texts for the Telegram bot."""

from __future__ import annotations


DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ("ru", "en")

MENU_LABELS = {
    "services": {"ru": "📦 Услуги", "en": "📦 Services"},
    "order": {"ru": "🛒 Заказать", "en": "🛒 Order"},
    "contact": {"ru": "📞 Связаться", "en": "📞 Contact"},
    "ask_ai": {"ru": "💬 Попробовать", "en": "💬 Try Demo"},
}

TEXTS = {
    "ru": {
        "choose_language": "Выберите язык / Choose your language",
        "language_saved": "Язык сохранен: русский.",
        "welcome": "Здравствуйте! 👋\n\nЯ — AI-бот, который помогает бизнесу отвечать клиентам автоматически.\n\nЧто я умею:\n✅ Отвечаю 24/7 без задержек\n✅ Консультирую клиентов\n✅ Принимаю заявки\n✅ Не даю клиентам «уйти»\n\nНажмите ниже и попробуйте 👇",
        "services_header": "<b>Я могу заменить менеджера и автоматизировать общение с клиентами:</b>\n\n💬 Автоответы\n📋 FAQ\n🛒 Приём заказов\n📅 Запись клиентов\n\nРаботаю 24/7 без выходных.\n\n<b>Готовые варианты:</b>",
        "services_footer": "Нажмите на нужный вариант ниже, чтобы сразу оставить заявку.",
        "order_choose_service": "Выберите вариант, который хотите заказать:",
        "service_selected": "Вы выбрали: <b>{service}</b>.",
        "lead_name": "Как к вам обращаться?",
        "lead_phone": "Отправьте номер телефона кнопкой ниже или напишите его вручную.",
        "lead_request": "Коротко опишите вашу задачу, чтобы менеджер подготовил предложение.",
        "lead_success": "Спасибо! Заявка сохранена. Менеджер скоро свяжется с вами.",
        "contact_info": "Хотите такого же бота для вашего бизнеса? 💰\n\n👉 Бот отвечает как живой менеджер и не пропускает клиентов.\n\nНапишите:\n👉 {contact_handle}\n\nСделаю под ваш бизнес за {delivery_time}.\nСтартовая цена: {price_from}\n\n{contact}",
        "contact_button": "Оставить заявку",
        "contact_direct_button": "Написать в Telegram",
        "ask_ai_intro": "Напишите любой вопрос 👇\n\nНапример:\n- Сколько стоит услуга?\n- Какие у вас тарифы?\n- Как записаться?\n\nЯ отвечу как живой менеджер 🙂",
        "cancel": "Отмена",
        "cancelled": "Действие отменено. Возвращаю вас в главное меню.",
        "invalid_phone": "Не удалось распознать номер. Отправьте его в формате +79991234567 или нажмите кнопку отправки контакта.",
        "share_phone": "Отправить номер",
        "spam_warning": "Слишком много сообщений за короткое время. Подождите {seconds} сек.",
        "admin_only": "Эта команда доступна только администратору.",
        "stats_title": "<b>Статистика бота</b>",
        "ai_error": "Сейчас AI временно недоступен. Я сохранил ваш запрос, попробуйте еще раз чуть позже.",
        "unexpected_error": "Что-то пошло не так. Попробуйте еще раз.",
        "service_not_found": "Услуга не найдена. Выберите вариант еще раз.",
        "menu_shown": "Главное меню открыто.",
        "request_type_order": "Заказ",
        "request_type_lead": "Заявка",
        "new_message_admin": "Новое сообщение от пользователя",
    },
    "en": {
        "choose_language": "Choose your language / Выберите язык",
        "language_saved": "Language saved: English.",
        "welcome": "Hello! 👋\n\nI am an AI bot that helps businesses answer customers automatically.\n\nWhat I can do:\n✅ Reply 24/7 without delays\n✅ Consult customers\n✅ Capture leads\n✅ Stop customers from slipping away\n\nTap below and try it 👇",
        "services_header": "<b>I can replace a manager and automate customer communication:</b>\n\n💬 Auto replies\n📋 FAQ\n🛒 Order capture\n📅 Client booking\n\nI work 24/7 without days off.\n\n<b>Ready-made options:</b>",
        "services_footer": "Tap an option below to send a request right away.",
        "order_choose_service": "Choose the option you want to order:",
        "service_selected": "You selected: <b>{service}</b>.",
        "lead_name": "What is your name?",
        "lead_phone": "Send your phone number with the button below or type it manually.",
        "lead_request": "Please describe your request so the manager can prepare the best offer.",
        "lead_success": "Thank you! Your request has been saved. A manager will contact you soon.",
        "contact_info": "Want a bot like this for your business? 💰\n\n👉 The bot answers like a live manager and never misses customers.\n\nMessage:\n👉 {contact_handle}\n\nI can build one for your business in {delivery_time}.\nStarting price: {price_from}\n\n{contact}",
        "contact_button": "Leave a request",
        "contact_direct_button": "Message on Telegram",
        "ask_ai_intro": "Send any question 👇\n\nFor example:\n- How much does it cost?\n- What packages do you have?\n- How can I book?\n\nI will answer like a real manager 🙂",
        "cancel": "Cancel",
        "cancelled": "Action canceled. Returning you to the main menu.",
        "invalid_phone": "I could not recognize the phone number. Please send it as +15551234567 or use the contact button.",
        "share_phone": "Share phone",
        "spam_warning": "Too many messages in a short time. Please wait {seconds} sec.",
        "admin_only": "This command is available only to the admin.",
        "stats_title": "<b>Bot Statistics</b>",
        "ai_error": "AI is temporarily unavailable. I saved your request, please try again a bit later.",
        "unexpected_error": "Something went wrong. Please try again.",
        "service_not_found": "Service not found. Please choose a service again.",
        "menu_shown": "Main menu opened.",
        "request_type_order": "Order",
        "request_type_lead": "Lead",
        "new_message_admin": "New message from user",
    },
}


def normalize_language(language: str | None) -> str:
    """Convert a raw Telegram language code into ru or en."""

    if not language:
        return DEFAULT_LANGUAGE
    return "ru" if language.lower().startswith("ru") else "en"


def t(language: str | None, key: str, **kwargs: str) -> str:
    """Return a localized text string with optional formatting."""

    normalized = normalize_language(language)
    template = TEXTS.get(normalized, TEXTS[DEFAULT_LANGUAGE]).get(key)
    if template is None:
        template = TEXTS[DEFAULT_LANGUAGE][key]
    return template.format(**kwargs)


def menu_label(action: str, language: str | None) -> str:
    """Return the translated text for a main menu button."""

    normalized = normalize_language(language)
    return MENU_LABELS[action][normalized]


def menu_mapping() -> dict[str, str]:
    """Map all localized menu labels back to internal action names."""

    mapping: dict[str, str] = {}
    for action, labels in MENU_LABELS.items():
        for label in labels.values():
            mapping[label] = action
    return mapping


MENU_TEXT_TO_ACTION = menu_mapping()
CANCEL_LABELS = {TEXTS["ru"]["cancel"], TEXTS["en"]["cancel"]}
