from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Константы для этапов диалога
NAME, RATING, FEEDBACK = range(3)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Добро пожаловать в детский центр 'Менделеевская долина'! "
        "Пожалуйста, введите ваше имя."
    )
    return NAME

def get_name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    update.message.reply_text(
        "Спасибо! Теперь оцените качество наших услуг от 1 до 5."
    )
    return RATING

def get_rating(update: Update, context: CallbackContext) -> int:
    context.user_data['rating'] = update.message.text
    update.message.reply_text(
        "Спасибо за вашу оценку! Пожалуйста, оставьте ваши замечания или пожелания."
    )
    return FEEDBACK

def get_feedback(update: Update, context: CallbackContext) -> int:
    context.user_data['feedback'] = update.message.text
    user_data = context.user_data
    update.message.reply_text(
        f"Спасибо за ваш отзыв, {user_data['name']}! "
        f"Ваш рейтинг: {user_data['rating']}\n"
        f"Ваши комментарии: {user_data['feedback']}\n"
        "Мы ценим ваше мнение!"
    )

    # Здесь можно добавить код для сохранения отзыва в базу данных
    user_data.clear()
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Вы отменили процесс. Если хотите снова оставить отзыв, отправьте /start."
    )
    return ConversationHandler.END

def main() -> None:
    updater = Updater("YOUR_TOKEN", use_context=True)

    # Добавление обработчиков
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            RATING: [MessageHandler(Filters.text & ~Filters.command, get_rating)],
            FEEDBACK: [MessageHandler(Filters.text & ~Filters.command, get_feedback)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
