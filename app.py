# encoding=utf8
import telebot
import config, db_funcs

def botLogic():
    bot = telebot.TeleBot(config.API_TOKEN)
    @bot.message_handler(content_types=['text'])
    def subscribeTo(message):
        message_sender = str(message.chat.id)
        is_admin, message_text = db_funcs.isAdmin(message_sender), str(message.text)
        if message.text=="/start":
            bot.send_message(message.chat.id, "Добро пожаловать в Excel-бот!")
        elif message.text=="/help":
            bot.send_message(message.chat.id, "<b>Доступны команды:</b>\nДобавить нового админа - <code>админ:добавить:*id админа*</code>\nУдалить админа - <code>админ:удалить:*id админа*</code>\nУзнать свой id - <code>id:</code>\nПоиск по ФИО - <code>поиск:фио:*ФИО работника*</code>\nВывести всех работников в отделе - <code>поиск:отдел:*название отдела*</code>\nПоиск по номеру карты - <code>поиск:карта:*номер карты*</code>\n",parse_mode='HTML')
            bot.send_message(message.chat.id, "Также можно проводить поиск введя ключевые слова:\n<code>*ФИО сотрудника*</code>,\n<code>*название группы*</code>,\n<code>*номер карты*</code>,\nоднако для большей скорости и точности следует использовать команды выше", parse_mode="HTML")
        elif message_text.startswith("админ:") and is_admin:
            bot.send_message(message.chat.id, db_funcs.changeAdmin(message_text))
        elif message_text.startswith("id:"):
            bot.send_message(message.chat.id, f"Ваш ID: {message_sender}")
        elif message_text.startswith("поиск:") and is_admin:
            bot.send_message(message.chat.id, db_funcs.searchByParam(message_text),parse_mode='HTML')
        elif db_funcs.isAdmin(message_sender):
            bot.send_message(message.chat.id, db_funcs.searchReg(message_text),parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "Недостаточно прав!")
    bot.polling(none_stop=True)
if __name__ == "__main__":
    db_funcs.initDB()
    print("Init complete...")
    botLogic()
