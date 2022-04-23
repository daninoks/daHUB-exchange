#!/usr/bin/env python
import textwrap


# def lang_list():
#     lang_list = ["eng", "rus"]
#     return lang_list


def start_mess(update, up):
    welcome_mess = ""
    if(up.get_lang(update.message.chat.id) == "eng"):
        welcome_mess = textwrap.dedent(f"""
                        Hello, {update.message.chat.first_name} !
                        Welcome to da-hub exchange bot
                        Here you can buy? sell? exchange? crypto
                        Here you can select different /language if need it.
                        Or just tap login to check your account status.
                        If you already signed in - feel free to go /exchange.

                        Any questions left? -- try: /FAQ & /support.
                        REPORT BUG: /bug_report.
                        /help - display welcome message above.
                        """)
    if(up.get_lang(update.message.chat.id) == "rus"):
        welcome_mess = textwrap.dedent(f"""
                        Приветствую, {update.message.chat.first_name} !
                        Добро пожаловать в da-hub exchange bot
                        Тут ты можешь купить, продать и обменять криптовалюты
                        """)
    return welcome_mess


# def start_mess(update, ep):
#     welcome_mess = ""
#     if(ep.lang == "eng"):
#         welcome_mess = textwrap.dedent(f"""
#                         Hello, {update.message.chat.first_name} !
#                         Welcome to da-hub exchange bot
#                         Here you can buy? sell? exchange? crypto
#                         Here you can select different /language if need it.
#                         Or just tap login to check your account status.
#                         If you already signed in - feel free to go /exchange.
#
#                         Any questions left? -- try: /FAQ & /support.
#                         REPORT BUG: /bug_report.
#                         /help - display welcome message above.
#                         """)
#     if(ep.lang == "rus"):
#         welcome_mess = textwrap.dedent(f"""
#                         Приветствую, {update.message.chat.first_name} !
#                         Добро пожаловать в da-hub exchange bot
#                         Тут ты можешь купить? продать? обменять? криптовалюты
#                         С помощью команды /language можешь поменять язык, если требуется.
#                         Или просто жми login чтобы проверить статус аккаунта.
#                         Если ты уже зарегистрирован - переходи к обмену: /exchange.
#
#                         Остались вопросы? -- поищи ответы: /FAQ или обратись в  /support.
#                         Нашел BUG?: /bug_report.
#                         /help - Отобразит данное письмо.
#                         """)
#     return welcome_mess


def support_mess(update, up):
    support_mess = ""
    if(up.get_lang(update.message.chat.id) == "eng"):
        support_mess = textwrap.dedent("""
        Here you can contact supprot.
        Use link bellow for now:
        """)
    if(up.get_lang(update.message.chat.id) == "rus"):
        support_mess = textwrap.dedent("""
        Тут можно обратиться в поддружку.
        Для этого используй ссылку ниже:
        """)
    return support_mess


def exchange_mess(update, up):
    log_in_mess = ""
    if(up.get_lang(update.message.chat.id) == "eng"):
        log_in_mess = textwrap.dedent(f"""
            Choose currency:
            Pay: {up.get_pay_cur(update.message.chat.id)}
            Get: {up.get_get_cur(update.message.chat.id)}
            """)
    if(up.get_lang(update.message.chat.id) == "rus"):
        log_in_mess = textwrap.dedent(f"""
            Выбери пару валют:
            Отправить: {up.get_pay_cur(update.message.chat.id)}
            Получить: {up.get_get_cur(update.message.chat.id)}
            """)
    return log_in_mess
