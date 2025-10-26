import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaAnimation
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

TOKEN = "8285756176:AAEQNxrmwdRgz9X7YU0q0PVxgJNdnsdN4Cc"

# Хранилище стадий для каждого пользователя
user_stage = {}

wrong_answers = [
    "Провал Броска! Это неверный путь! Твоя интуиция тебя подводит.",
    "Не-е-ет! Иллюзия держится! Повтори свой поиск, Герой.",
    "Не то! Твой свиток предсказаний оказался пуст. Попробуй другую формулу.",
    "Слишком просто. Это лишь обманка! Магия сложнее, чем кажется.",
    "Ошибка в расчетах! Ответ не совпал с формулой. Повтори анализ, быстро!"
]

# Старт команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_stage[user_id] = 0

    keyboard = [[InlineKeyboardButton("Начать квест 🗡️", callback_data="start_quest")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_animation(
        animation=open("Gif-1.gif", "rb"),
        caption=(
            "<b>Ох, приветствую тебя, Андрей, Завоеватель Трех с Половиной Десятилетий!</b>\n\n"
            "Я, <b>Магистр Флавиус Абессинский</b>, Архимаг Школы Трансмутации и <b>Небесный Предсказатель Скидок</b>, "
            "прозреваю сквозь туманы измерений, чтобы узреть твое великое... <b>повышение уровня</b>!\n\n"
            "Желаю <b>Критических Успехов</b> во всех делах, бесконечного запаса <b>Хит Поинтов</b> для здоровья и <b>золота</b>, "
            "чтобы всегда хватало на лучшие зелья и артефакты. Пусть каждый твой день дарит <b>Легендарный лут</b>! С 35-м уровнем!\n\n"
            "Твоя доблестная душа и заслуженный возраст притягивают не только драконов, но и сокровища! "
            "Я, Магистр Флавиус, сообщаю: твои подарки не достанутся тебе легко. "
            "Они запечатаны <b>Мощным Заклинанием Временного Смещения</b>, которое можно снять только выполнив <b>Квест Дня Рождения</b>!\n\n"
            "Собери свой отряд, заточи <b>Меч Острых Шуток</b> и отправляйся! "
            "И помни: каждый выполненный этап Квеста дает не только <b>Опыт</b>, но и <b>Часть Награды</b>!\n"
            "Да пребудет с тобой <b>Критический Успех</b> в поисках! 🏹"
        ),
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# Обработка нажатий кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    stage = user_stage.get(user_id, 0)

    if query.data == "start_quest" and stage == 0:
        user_stage[user_id] = 1
        # Сообщение для Задания 1
        await query.message.reply_text(
            "<b>Андрей, ты принял вызов! Мудро!</b> Но для начала, ты должен доказать, что глаз твой остер, а память о Твоем Личном Подземелье — безупречна.\n\n"
            "<b>ЗАДАНИЕ 1: ИСПЫТАНИЕ НАБЛЮДАТЕЛЬНОСТИ</b>\n"
            "Я использовал свое могущественное <b>Заклинание Иллюзии 4-го Круга</b> и слегка изменил одну фотографию, на которой изображен угол твоего мирного убежища. "
            "Это уголок, который ты видишь постоянно, почти на уровне подсознания.\n\n"
            "Твоя задача, Герой: Взгляни на присланный образ. Что не так? Какой <b>Важный Артефакт</b>, который должен быть на этом месте, был временно изгнан из этого Измерения моей магией?\n\n"
            "Удачи, <b>Искатель Сокровищ</b>! Да будет твоя проницательность так же остра, как когти! 🐾",
            parse_mode="HTML"
        )
        with open("Photo-1.jpg", "rb") as photo:
            await query.message.reply_photo(photo=photo, has_spoiler=True)

# Обработка текстовых сообщений
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    stage = user_stage.get(user_id, 0)
    text = update.message.text.strip()

    # Задание 1
    if stage == 1:
        if text.lower() == "криминальное чтиво":
            user_stage[user_id] = 2
            await update.message.reply_text(
                "<b>БРАВО, АНДРЕЙ!</b> Твой <b>Бросок на Интеллект</b> успешен, <b>Критический Успех</b>! Ты прорвался сквозь мои чары! Задание выполнено!\n"
                "Но не расслабляйся! Твое следующее испытание требует <b>Кошачьей Перспективы</b>!\n\n"
                "<b>ЗАДАНИЕ 2: ТОЧКА ЗРЕНИЯ АРТЕФАКТА</b>\n"
                "Я использовал <b>Заклинание Смещения Души</b> и временно поместил один из твоих подарков в... необычное место.\n"
                "Твоя задача: Найти место в твоем <b>Логове</b>, где сейчас находится этот тайный Артефакт!\n"
                "Ориентируйся по потолку, полу, мебели! Думай, как <b>Спящий Кот</b>, который наблюдает за миром из своего укромного места! 🐱",
                parse_mode="HTML"
            )
            with open("Photo-2.jpg", "rb") as photo:
                await update.message.reply_photo(photo=photo, has_spoiler=True)
        else:
            await update.message.reply_text(random.choice(wrong_answers))

    # Задание 2
    elif stage == 2:
        if text.lower() == "марсель":
            user_stage[user_id] = 3
            await update.message.reply_text(
                "<b>БЛЕСТЯЩЕ, АНДРЕЙ!</b> Ты обладаешь <b>Повышенным Интеллектом</b> замлуженно! "
                "Ты верно отгадал шараду! Задание 2 выполнено!\n\n"
                "<b>ЗАДАНИЕ 3: ТАКТИЛЬНОЕ ИСПЫТАНИЕ</b>\n"
                "Я использовал <b>Заклинание Трансмутации Поверхности</b> и слил твой последний спрятанный дар с окружающей средой!\n"
                "Твоя задача: Найти этот узор в твоей квартире! Последний Подарок спрятан именно <b>В ЭТОМ МЕСТЕ</b>, слившись с ним!\n"
                "Сконцентрируй свою <b>Магию Осязания</b>! Думай, как Кот, который выбирает самое мягкое и незаметное место для сна! 🐾",
                parse_mode="HTML"
            )
            with open("Photo-3.jpg", "rb") as photo:
                await update.message.reply_photo(photo=photo, has_spoiler=True)
        else:
            await update.message.reply_text(random.choice(wrong_answers))

    # Задание 3
    elif stage == 3:
        if text == "7":
            user_stage[user_id] = 4
            await update.message.reply_text(
                "<b>ВОСХИТИТЕЛЬНО, АНДРЕЙ!</b> Твоя <b>Логика</b> на уровне Эльфа-Ясновидца! Ты победил! Задание выполнено!\n"
                "Но теперь ты стоишь перед <b>Сундуком Сокровищ</b>! Он заперт древним Замком Чисел, который откроет только верный код!\n\n"
                "<b>ФИНАЛЬНОЕ ИСПЫТАНИЕ: ЛАБИРИНТ ХРАНИТЕЛЯ КОДА</b>\n"
                "Перед тобой лежит <b>Лабиринт</b>, начертанный на листе (или экране). "
                "Собери цифры в правильном порядке, чтобы получить <b>Код из 3 Знаков</b>! "
                "Сконцентрируй свою <b>Ловкость и Интеллект</b>! Только верный код откроет Сундук! 🗝️",
                parse_mode="HTML"
            )
            with open("Photo-4.jpg", "rb") as photo:
                await update.message.reply_photo(photo=photo, has_spoiler=True)
        else:
            await update.message.reply_text(random.choice(wrong_answers))

    # Финальное задание
    elif stage == 4:
        if text == "99":
            user_stage[user_id] = 5
            await update.message.reply_text(
                "<b>ВОСХИТИТЕЛЬНО, АНДРЕЙ!</b> Твоя <b>Ловкость и Интеллект</b> преодолели это испытание! "
                "Счетчик Квеста показывает: <b>ПОБЕДА!</b>\n\n"
                "<b>ФИНАЛЬНЫЙ АКТ: КООРДИНАТЫ ГЛАВНОГО АРТЕФАКТА</b>\n"
                "Твоя цель — <b>Главный Артефакт</b> — находится РЯДОМ! Так близко, как никогда!\n"
                "Я присылаю тебе <b>Трио Предвестников</b>! Твоя задача: найти место, где ВСЕ ТРИ ПРЕДМЕТА сходятся на Карте Твоего Дома!\n"
                "Именно там, в Центре Притяжения этих Артефактов, лежит <b>ТВОЙ ФИНАЛЬНЫЙ, СИЯЮЩИЙ, ЛЕГЕНДАРНЫЙ ПОДАРОК</b>! 🏆\n"
                "Да пребудет с тобой <b>Инстинкт и Бонус к Скорости Движения</b>! МИССИЯ завершится, как только ты заберешь свою <b>Награду 35-го Уровня</b>!",
                parse_mode="HTML"
            )
            with open("Photo-4.jpg", "rb") as photo:
                await update.message.reply_photo(photo=photo, has_spoiler=True)
        else:
            await update.message.reply_text(random.choice(wrong_answers))

    # После завершения квеста любое сообщение
    elif stage == 5:
        keyboard = [[InlineKeyboardButton("Да, я выполнил все задания ✅", callback_data="finished")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Что ты тут ищешь, Андрей? Твой <b>Журнал Квестов</b> должен быть пуст, а <b>Инвентарь</b> — полон! "
            "Ты завершил все Испытания? Нашел <b>Финальный Артефакт</b>?\nВремя не ждет! Отвечай, воин! ⚔️",
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("Используй /start, чтобы начать квест.")

# Обработка нажатия кнопки "Да, я выполнил все задания"
async def finished_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_animation(
        animation=open("Gif-2.gif", "rb"),
        caption=(
            "СЛУШАЙТЕ И ВНИМАЙТЕ, ЖИТЕЛИ ВСЕХ ИЗМЕРЕНИЙ! 🌌\n"
            "<b>АНДРЕЙ, ТИТАН 35-ГО УРОВНЯ</b>, ОФИЦИАЛЬНО ЗАВЕРШИЛ ЭПИЧЕСКУЮ КАМПАНИЮ ДНЯ РОЖДЕНИЯ!\n"
            "Его <b>Интеллект</b> преодолел иллюзии, <b>Ловкость</b> обошла ловушки, а <b>Мудрость</b> привела к Финальному Луту! "
            "Ты доказал, что являешься Истинным Властелином своего <b>Логова</b>! Твой Счет Опыта сегодня достиг легендарных высот!\n\n"
            "Пусть твой <b>Модификатор Харизмы</b> очаровывает всех союзников, твой <b>Спасбросок от Усталости</b> всегда будет успешен, "
            "а твоя <b>Куча Золота</b> никогда не уменьшается!\n\n"
            "МЫ САЛЮТУЕМ ТЕБЕ, АНДРЕЙ! Отпразднуй свою Победу с честью и изобилием! 🎉\n"
            "<b>С ДНЕМ РОЖДЕНИЯ!</b>"
        ),
        parse_mode="HTML"
    )

# Основная функция
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^start_quest$"))
    app.add_handler(CallbackQueryHandler(finished_handler, pattern="^finished$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("🔥 Бот запущен! Нажми Ctrl+C, чтобы остановить.")
    app.run_polling()
