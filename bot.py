#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Telegram-бот для квеста на День Рождения.
Создан на основе python-telegram-bot.
"""

import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ParseMode

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота
TOKEN = "8285756176:AAEQNxrmwdRgz9X7YU0q0PVxgJNdnsdN4Cc"

# Определяем состояния для ConversationHandler
(
    START_QUEST,
    AWAIT_TASK_1,
    AWAIT_TASK_2,
    AWAIT_TASK_3,
    AWAIT_TASK_4,
    AWAIT_TASK_5,
    AWAIT_FINAL_CONFIRM,
    QUEST_FINISHED,
) = range(8)

# Список случайных ответов при ошибке
WRONG_ANSWERS = [
    "<b>Провал Броска!</b> Это неверный путь! Твоя интуиция тебя подводит. 😵‍💫",
    "<b>Не-е-ет! Иллюзия держится!</b> Повтори свой поиск, Герой. 🕵️‍♂️",
    "<b>Не то!</b> Твой свиток предсказаний оказался пуст. Попробуй другую формулу. 📜",
    "<b>Слишком просто.</b> Это лишь обманка! Магия сложнее, чем кажется. 🌀",
    "<b>Ошибка в расчетах!</b> Ответ не совпал с формулой. Повтори анализ, быстро! 🧠",
]


async def wrong_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет случайное сообщение об ошибке."""
    await update.message.reply_text(
        random.choice(WRONG_ANSWERS), parse_mode=ParseMode.HTML
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 1: /start. Отправляет приветствие, GIF-1 и кнопку."""
    keyboard = [
        [InlineKeyboardButton("Начать квест", callback_data="start_quest")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "Ох, приветствую тебя, Андрей, Завоеватель Трех с Половиной Десятилетий! 🥳\n\n"
        "Я, Магистр Флавиус Абессинский, Архимаг Школы Трансмутации и Небесный Предсказатель Скидок, прозреваю сквозь туманы измерений, чтобы узреть твое великое... <b>повышение уровня!</b> 🌟\n\n"
        "Желаю <b>Критических Успехов</b> во всех делах, бесконечного запаса <b>Хит Поинтов</b> для здоровья и золота, чтобы всегда хватало на лучшие зелья и артефакты. 💎 Пусть каждый твой день дарит <b>Легендарный лут!</b> С 35-м уровнем! 🎂\n\n"
        "Твоя доблестная душа и заслуженный возраст притягивают не только драконов, но и сокровища! 🐲 Я, Магистр Флавиус, сообщаю: твои подарки не достанутся тебе легко. Они запечатаны <b>Мощным Заклинанием Временного Смещения</b>, которое можно снять только выполнив <b>Квест Дня Рождения!</b> 📜\n\n"
        "Собери свой отряд, заточи <b>Меч Острых Шуток</b> и отправляйся! И помни: каждый выполненный этап Квеста дает не только <b>Опыт</b>, но и <b>Часть Награды!</b> 💰\n"
        "Да пребудет с тобой <b>Критический Успех</b> в поисках!”"
    )

    await update.message.reply_animation(
        animation=open("Gif-1.gif", "rb"),
        caption=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
    )
    return START_QUEST


async def start_quest_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 2: Нажата кнопка 'Начать квест'. Отправляет Задание 1."""
    query = update.callback_query
    await query.answer()
    # Убираем кнопку из предыдущего сообщения
    await query.edit_message_reply_markup(reply_markup=None)

    text = (
        "Андрей, ты принял вызов! Мудро! 🧠 Но для начала, ты должен доказать, что глаз твой остер, а память о <b>Твоем Личном Подземелье</b> — безупречна. ✨\n\n"
        "<b>ЗАДАНИЕ 1: ИСПЫТАНИЕ НАБЛЮДАТЕЛЬНОСТИ</b> 🧐\n"
        "Я использовал свое могущественное <b>Заклинание Иллюзии 4-го Круга</b> и слегка изменил одну фотографию, на которой изображен угол твоего мирного убежища. Это уголок, который ты видишь постоянно, почти на уровне подсознания. 👁️\n\n"
        "Твоя задача, Герой: Взгляни на присланный образ. <b>Что не так?</b>\n"
        "<b>Какой Важный Артефакт</b>, который должен быть на этом месте, был временно изгнан из этого Измерения моей магией? 🔮\n\n"
        "Удачи, Искатель Сокровищ! Да будет твоя проницательность так же остра, как когти! 🦅"
    )

    await context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=open("Photo-1.jpg", "rb"),
        caption=text,
        has_spoiler=True,
        parse_mode=ParseMode.HTML,
    )
    return AWAIT_TASK_1


async def task_1_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 3: Обработка ответа на Задание 1. Ждет 'Криминальное чтиво'."""
    answer = update.message.text
    if answer.strip().lower() == "криминальное чтиво":
        text = (
            "<b>БРАВО, АНДРЕЙ!</b> Твой <b>Бросок на Интеллект</b> успешен, <b>Критический Успех!</b> 🎯 Ты прорвался сквозь мои чары! Задание выполнено! ✅\n\n"
            "Но не расслабляйся! Твое следующее испытание требует <b>Кошачьей Перспективы!</b> 🐱\n\n"
            "<b>ЗАДАНИЕ 2: ТОЧКА ЗРЕНИЯ АРТЕФАКТА</b> 👁️\n"
            "Я использовал <b>Заклинание Смещения Души</b> и временно поместил один из твоих подарков в... необычное место. 🎁\n\n"
            "Тебе будет отправлено изображение. Но это не просто рисунок! Это ракурс, который видит только твой подарок. <b>Ты смотришь на мир его глазами!</b>\n\n"
            "Твоя задача: <b>Найти место в твоем Логове</b>, где сейчас находится этот тайный Артефакт! 🗺️\n\n"
            "Ориентируйся по потолку, полу, мебели! Думай, как <b>Спящий Кот</b>, который наблюдает за миром из своего укромного места! 💤\n\n"
            "Да будет твое зрение острым, а интуиция – мурчащей! Вперед!"
        )

        await update.message.reply_photo(
            photo=open("Photo-2.jpg", "rb"),
            caption=text,
            has_spoiler=True,
            parse_mode=ParseMode.HTML,
        )
        return AWAIT_TASK_2
    else:
        await wrong_answer(update, context)
        return AWAIT_TASK_1


async def task_2_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 4: Обработка ответа на Задание 2. Ждет 'Марсель'."""
    answer = update.message.text
    if answer.strip().lower() == "марсель":
        text = (
            "<b>БЛЕСТЯЩЕ, АНДРЕЙ!</b> Ты обладаешь <b>Повышенным Интеллектом</b> замлуженно! 💡 Ты верно отгадал шараду! Задание 2 выполнено! ✅\n\n"
            "Но следующая награда требует ещё большего усилия! 💪\n\n"
            "<b>ЗАДАНИЕ 3: ТАКТИЛЬНОЕ ИСПЫТАНИЕ</b> 🖐️\n"
            "Я использовал свое <b>Заклинание Трансмутации Поверхности</b> и слил твой последний спрятанный дар с окружающей средой! 🌿\n\n"
            "Тебе будет отправлена фотография <b>крупного плана уникальной текстуры</b> в твоем Логове. 🖼️\n\n"
            "Твоя задача: <b>Найти этот узор в твоей квартире!</b> Последний Подарок спрятан именно <b>В ЭТОМ МЕСТЕ</b>, слившись с ним! 🤫\n\n"
            "Сконцентрируй свою <b>Магию Осязания!</b> Думай, как <b>Кот</b>, который выбирает самое мягкое и незаметное место для сна! 😴\n\n"
            "Да пребудет с тобой <b>Критический Успех</b> в осязании!"
        )

        await update.message.reply_photo(
            photo=open("Photo-3.jpg", "rb"),
            caption=text,
            has_spoiler=True,
            parse_mode=ParseMode.HTML,
        )
        return AWAIT_TASK_3
    else:
        await wrong_answer(update, context)
        return AWAIT_TASK_2


async def task_3_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 5: Обработка ответа на Задание 3. Ждет '7'."""
    answer = update.message.text
    if answer.strip() == "7":
        text = (
            "<b>ВОСХИТИТЕЛЬНО, АНДРЕЙ!</b> Твоя <b>Мягкая как кошачья лапка Логика</b>\n"
            "на уровне Эльфа-Ясновидца! 🧠 Ты победил! Задание выполнено! ✅\n\n"
            "Но теперь ты стоишь перед <b>Сундуком Сокровищ!</b> 📦 Он заперт древним <b>Замком Чисел</b>, который откроет только верный код! 🔐\n\n"
            "<b>ФИНАЛЬНОЕ ИСПЫТАНИЕ: ЛАБИРИНТ ХРАНИТЕЛЯ КОДА</b> 🗺️\n"
            "Перед тобой лежит Лабиринт, начертанный на листе (или экране). Это <b>Проклятый Лабиринт Флавиуса</b>, где все пути ведут к истине.\n\n"
            "Твоя задача: <b>Пройти лабиринт от старта до финиша 3 раза.</b>\n"
            "<b>Собери цифры в правильном порядке</b>, чтобы получить <b>Код из 3 Знаков!</b> 🔢\n\n"
            "Сконцентрируй свою <b>Ловкость и Интеллект!</b> Только верный код отопрет Сундук, где тебя ждет <b>Легендарный Лут Героя 35-го Уровня!</b> 🏆\n\n"
            "Да будет твоя рука тверда, а взгляд — чист! ✨"
        )

        await update.message.reply_photo(
            photo=open("Photo-4.jpg", "rb"),
            caption=text,
            has_spoiler=True,
            parse_mode=ParseMode.HTML,
        )
        return AWAIT_TASK_4
    else:
        await wrong_answer(update, context)
        return AWAIT_TASK_3


async def task_4_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 6: Обработка ответа на Задание 4. Ждет '99'."""
    answer = update.message.text
    if answer.strip() == "99":
        text = (
            "<b>ВОСХИТИТЕЛЬНО, АНДРЕЙ!</b> Твоя <b>Ловкость и\n"
            "Интеллект</b> преодолели и это испытание! 🚀 Счетчик Квеста показывает: <b>ПОБЕДА!</b> 🏁\n\n"
            "Ты чувствуешь, как энергия последнего <b>ГЛАВНОГО Сундука</b>\n"
            "пульсирует... 💥 Но <b>Финальный Лут</b> не так прост!\n\n"
            "<b>ФИНАЛЬНЫЙ АКТ: КООРДИНАТЫ ГЛАВНОГО АРТЕФАКТА</b> 📍\n"
            "Твоя цель — <b>Главный Артефакт</b> — находится <b>РЯДОМ!</b> Так близко, как никогда! 🤩\n\n"
            "Я присылаю тебе <b>Трио Предвестников!</b> Ты знаешь <b>Точки Респауна</b> этих предметов? 🤔\n\n"
            "Твоя задача, Герой: <b>Отправляйся в Зону Наибольшего Сближения!</b> Найди то место, где <b>ВСЕ ТРИ ПРЕДМЕТА</b> сходятся на <b>Карте Твоего Дома!</b> 🗺️\n\n"
            "Именно там, в <b>Центре Притяжения</b> этих Артефактов, лежит ТВОЙ <b>ФИНАЛЬНЫЙ, СИЯЮЩИЙ, ЛЕГЕНДАРНЫЙ ПОДАРОК!</b> 🎁✨\n\n"
            "Да пребудет с тобой <b>Инстинкт</b> и <b>Бонус к Скорости Движения!</b>\n"
            "<b>МИССИЯ</b> завершится, как только ты заберешь свою <b>Награду 35-го Уровня!</b> 🏆"
        )

        await update.message.reply_photo(
            photo=open("Photo-5.jpg", "rb"),
            caption=text,
            has_spoiler=True,
            parse_mode=ParseMode.HTML,
        )
        return AWAIT_TASK_5
    else:
        await wrong_answer(update, context)
        return AWAIT_TASK_4


async def task_5_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 7: Любое сообщение после Задания 5. Спрашивает, закончил ли."""
    keyboard = [
        [InlineKeyboardButton("Да, я выполнил все задания", callback_data="finish_quest")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "ЭЙ! ТЫ! <b>ГЕРОЙ 35-ГО УРОВНЯ!</b> 📣\n"
        "Что ты тут ищешь, Андрей? Твой <b>Журнал Квестов</b> должен быть пуст, а <b>Инвентарь</b> — полон! 📜 Ты завершил все Испытания? Нашел <b>Финальный Артефакт?</b> 🎁\n"
        "Время не ждет! Отвечай, воин! ⏳"
    )

    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
    )
    return AWAIT_FINAL_CONFIRM


async def finish_quest_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 8: Нажата кнопка 'Да, я выполнил...'. Отправляет Gif-2 и поздравление."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)  # Убираем кнопку

    text = (
        "<b>СЛУШАЙТЕ И ВНИМАЙТЕ, ЖИТЕЛИ ВСЕХ ИЗМЕРЕНИЙ!</b> 📢\n"
        "<b>АНДРЕЙ, ТИТАН 35-ГО УРОВНЯ, ОФИЦИАЛЬНО ЗАВЕРШИЛ ЭПИЧЕСКУЮ КАМПАНИЮ ДНЯ РОЖДЕНИЯ!</b> 🏆\n\n"
        "Его <b>Интеллект</b> преодолел иллюзии, <b>Ловкость</b> обошла ловушки, а <b>Мудрость</b> привела к <b>Финальному Луту!</b> ✨ Ты доказал, что являешься <b>Истинным\n"
        "Властелином своего Логова!</b> 👑 Твой <b>Счет Опыта</b> сегодня достиг легендарных высот! 📈\n\n"
        "Пусть твой <b>Модификатор Харизмы</b> очаровывает всех союзников, 🥰 твой <b>Элексир от Усталости</b> всегда будет действовать, а твоя <b>Казка, Милорд</b>, никогда не опустеет! 💰\n\n"
        "<b>МЫ САЛЮТУЕМ ТЕБЕ, АНДРЕЙ!</b> Отпразднуй свою Победу с честью и изобилием! 🥳\n"
        "<b>С ДНEM РОЖДЕНИЯ!</b> 🎂"
    )

    await context.bot.send_animation(
        chat_id=query.message.chat_id,
        animation=open("Gif-2.gif", "rb"),
        caption=text,
        parse_mode=ParseMode.HTML,
    )
    return QUEST_FINISHED


async def after_finish_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 9: Любые сообщения после завершения квеста."""
    text = (
        "Ты ищешь меня? Увы, я не нахожусь в твоем Измерении! 💨\n"
        "Как только <b>Финальный Лут</b> был добыт, мой <b>Сосуд Маны</b> опустел. 📉 Я активировал <b>Заклинание Экстренного Отступления</b> (Emergency Retreat) и сейчас восстанавливаю <b>Очки Маны</b> в <b>Астральном Трактире \"Спящий Кот\"!</b> 😴\n\n"
        "Мой <b>Договор Исполнен!</b> 📜 Твой <b>Квест Завершен!</b> Ты свободен! Я вернусь, когда соберу достаточно <b>Реагентов</b> для следующего <b>Эпического Приключения!</b> 🧙‍♂️\n\n"
        "Продолжай свое героическое существование! 🛡️"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)
    return QUEST_FINISHED


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет квест."""
    await update.message.reply_text(
        "Квест прерван! Магистр Флавиус отступает в свое измерение... 🧙‍♂️"
    )
    return ConversationHandler.END


def main() -> None:
    """Запуск бота."""
    application = Application.builder().token(TOKEN).build()

    # Создаем ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_QUEST: [
                CallbackQueryHandler(start_quest_callback, pattern="^start_quest$")
            ],
            AWAIT_TASK_1: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, task_1_handler)
            ],
            AWAIT_TASK_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, task_2_handler)
            ],
            AWAIT_TASK_3: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, task_3_handler)
            ],
            AWAIT_TASK_4: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, task_4_handler)
            ],
            AWAIT_TASK_5: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, task_5_handler)
            ],
            AWAIT_FINAL_CONFIRM: [
                CallbackQueryHandler(finish_quest_callback, pattern="^finish_quest$")
            ],
            QUEST_FINISHED: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, after_finish_handler)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Запускаем бота
    application.run_polling()


if __name__ == "__main__":

    main()

