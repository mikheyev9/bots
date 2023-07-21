from cores_src.telecore import TeleCore

core = TeleCore()
core.start()


@core.bot.message_handler(content_types=['text'])
def get_message(message):
    print(f'{message.from_user.username} ({message.from_user.id}): {message.text}')


core.bot.polling(non_stop=True)
