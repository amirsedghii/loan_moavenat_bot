from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# مراحل
AGE, LICENSE, NEED, CAPITAL, LOCATION = range(5)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! فرم ارزیابی وام شروع شد.\nسن خود را وارد کنید:")
    return AGE

def age(update: Update, context: CallbackContext):
    context.user_data['age'] = int(update.message.text)
    update.message.reply_text("وضعیت مجوز فعالیت خود را انتخاب کنید:\nدارم / در حال دریافت / ندارم")
    return LICENSE

def license(update: Update, context: CallbackContext):
    context.user_data['license'] = update.message.text
    update.message.reply_text("مبلغ مورد نیاز برای طرح (تومان) را وارد کنید:")
    return NEED

def need(update: Update, context: CallbackContext):
    context.user_data['need'] = int(update.message.text)
    update.message.reply_text("سرمایه اولیه شما (تومان) را وارد کنید:")
    return CAPITAL

def capital(update: Update, context: CallbackContext):
    context.user_data['capital'] = int(update.message.text)
    update.message.reply_text("محل اجرای طرح (شهر/استان) را وارد کنید:")
    return LOCATION

def location(update: Update, context: CallbackContext):
    context.user_data['location'] = update.message.text

    # محاسبه واجد شرایط بودن
    age = context.user_data['age']
    license_status = context.user_data['license']
    need = context.user_data['need']
    capital = context.user_data['capital']

    if 23 <= age <= 60 and license_status != "ندارم" and capital >= need * 0.3:
        result = "✅ شما واجد شرایط اولیه دریافت تسهیلات هستید."
    else:
        result = "❌ شرایط لازم برای دریافت تسهیلات را ندارید."

    update.message.reply_text(result)
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("فرم ارزیابی لغو شد.")
    return ConversationHandler.END

def main():
    TOKEN = " 8576615984:AAF_9G4hALcZM5UPygesonGwq6Q4vK6HjkA" 
    updater = "100915363"
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGE: [MessageHandler(Filters.text & ~Filters.command, age)],
            LICENSE: [MessageHandler(Filters.text & ~Filters.command, license)],
            NEED: [MessageHandler(Filters.text & ~Filters.command, need)],
            CAPITAL: [MessageHandler(Filters.text & ~Filters.command, capital)],
            LOCATION: [MessageHandler(Filters.text & ~Filters.command, location)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()