#!/usr/bin/env python

import logging
import textwrap
import re

from typing import List, Tuple, cast
from telegram import (
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    Bot,
    BotCommand,
)
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    InvalidCallbackData,
    PicklePersistence,
    Dispatcher,
    MessageHandler
)

from telegram.utils import helpers

from mySQLconnector import pullDB
import langMessLib
from dynamicClass import UserPropeties as UserPropeties

# BackEnd User Params:
API_TOKEN = '5229570403:AAE6ToddCPzgn9Xy62oG4Pv82Ga75B8nLrU'
SUPPORT_BOT_URL = "https://t.me/DaHubSupportBot"

# bot commands without scope yet.
Bot(API_TOKEN).set_my_commands([
        BotCommand('start', 'start page'),
        BotCommand('language', 'change lang'),
        BotCommand('exchange', 'go trade'),
        BotCommand('faq', 'FAQ link'),
        BotCommand('help', 'display help mess'),
        BotCommand('support', 'support/support inbot order'),
        BotCommand('bug', 'report bug to bug channel')
])


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Interraction tree:
FIRST, SECOND = range(2)
# Callback data
LOG_IN = "log_in"
GO_SELECT_PAY = "exchange"
PENDING = "pending"
SHARE = "share"
# SUPPORT = "support"
SUPPORT_MENU = "support"
CONFIRM = "confirm"

LANG_ENG = "eng"
LANG_RUS = "rus"

BACK_START = "back_start"
BACK_LANG = "back_lang"
BACK_LOGIN = "back_login"
GO_MAINPAGE = "go_mainpage"

REFERAL = "referal"
GO_SETTINGS = "go_settings"
REQUISITES = "requisities"
GO_LANGUAGE = "go_language"
GO_INPUT_VALUE = "go_input_value"
GO_SELECT_GET = "go_select_get"

GO_LANGUAGE_SETTINGS = "go_lang_settings"
LANG_ENG_SETTINGS = "eng_lang_settings"
LANG_RUS_SETTINGS = "rus_lang_settings"


ep = emoji_fb = {'not_sel': '\U0000274c', 'sel': '\U00002714', 'empty': ''}

currency_dict = {
    "pay_cur": {
        "pay_usdt": {"name": "USDT", "status": emoji_fb['empty'], "id": "pay_usdt"},
        "pay_ton": {"name": "TON", "status": emoji_fb['empty'], "id": "pay_ton"},
        "pay_rub": {"name": "RUB", "status": emoji_fb['empty'], "id": "pay_rub"},
        "pay_egp": {"name": "EGP", "status": emoji_fb['empty'], "id": "pay_egp"},
    },
    "get_cur": {
        "get_usdt": {"name": "USDT", "status": emoji_fb['empty'], "id": "get_usdt"},
        "get_ton": {"name": "TON", "status": emoji_fb['empty'], "id": "get_ton"},
        "get_rub": {"name": "RUB", "status": emoji_fb['empty'], "id": "get_rub"},
        "get_egp": {"name": "EGP", "status": emoji_fb['empty'], "id": "get_egp"},
    }
}

numbers_keyboard = {
    "row1": {
        "cb_1": {"name": "1", "id": "cb_1"},
        "cb_2": {"name": "2", "id": "cb_2"},
        "cb_3": {"name": "3", "id": "cb_3"},
    },
    "row2": {
        "cb_4": {"name": "4", "id": "cb_4"},
        "cb_5": {"name": "5", "id": "cb_5"},
        "cb_6": {"name": "6", "id": "cb_6"},
    },
    "row3": {
        "cb_7": {"name": "7", "id": "cb_7"},
        "cb_8": {"name": "8", "id": "cb_8"},
        "cb_9": {"name": "9", "id": "cb_9"},
    },
    "row4": {
        "cb_clear": {"name": "<<clear", "id": "cb_clear"},
        "cb_0": {"name": "0", "id": "cb_0"},
        "cb_del": {"name": "<del", "id": "cb_del"},
    },
}


# class ExchangePanel:
#     def __init__(self, lang, pay_cur, get_cur, value_cur):
#         self.lang = lang
#         self.pay_cur = pay_cur
#         self.get_cur = get_cur
#         self.value_cur = value_cur

# COMMANDS FUNCTIONS:
def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    print(update)
    print(update.message.chat.id)
    print(up.get_lang(update.message.chat.id))

    welcome_mess = langMessLib.start_mess(update, up)
    # bot = context.bot
    # url = helpers.create_deep_linked_url(
    #     bot.username, 'check-this-out', group=True)

    keyboard = [
        [InlineKeyboardButton("Log In", callback_data=str(LOG_IN))],
        # [InlineKeyboardButton("Support", callback_data=str(SUPPORT_MENU))],
        # [InlineKeyboardButton("Share Bot", url=url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text=welcome_mess, reply_markup=reply_markup)
    return FIRST


# REDIRECTED FROM BUTTONS FUNCTIONS:
def start_over(update: Update, context: CallbackContext) -> int:
    """Send start message in inLine mode."""
    query = update.callback_query
    query.answer()

    welcome_mess = langMessLib.start_mess(update, ep)
    # bot = context.bot
    # url = helpers.create_deep_linked_url(
    #     bot.username, 'check-this-out', group=True)
    keyboard = [
        [InlineKeyboardButton("Log In", callback_data=str(LOG_IN))],
        # [InlineKeyboardButton("Support", callback_data=str(SUPPORT_MENU))],
        # [InlineKeyboardButton("Share Bot", url=url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=welcome_mess, reply_markup=reply_markup)
    return FIRST


def language_over(update: Update, context: CallbackContext) -> int:
    """Change system language"""
    query = update.callback_query
    query.answer()

    if(re.match(r'eng|rus', query.data)):
        up.set_lang(query.message.chat.id, query.data)
    language_mess = textwrap.dedent(f"""
        Select language / Выбрать язык
        Selected / Выбранный : {up.get_lang(query.message.chat.id)}""")
    keyboard = [
        [InlineKeyboardButton("ENG", callback_data=str(LANG_ENG)),
            InlineKeyboardButton("RUS", callback_data=str(LANG_RUS))],
        [InlineKeyboardButton("Continue", callback_data=str(GO_MAINPAGE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=language_mess, reply_markup=reply_markup)
    return FIRST


def main_page(update: Update, context: CallbackContext) -> int:
    """Log in to the System"""
    query = update.callback_query
    userObject = pullDB(query.message.chat.id)
    query.answer()

    log_in_mess = textwrap.dedent(f"""
        <Here can be posted info from userObject(actually from DB)>
        User ID: {userObject.userID}
        User SHA: {userObject.userToken}
        User Banned state: {userObject.userBanned}
        DataBase Status: {userObject.dbMessage}""")
    keyboard = [
        [InlineKeyboardButton("Exchange", callback_data=str(GO_SELECT_PAY))],
        [InlineKeyboardButton("Pending", callback_data=str(PENDING))],
        [InlineKeyboardButton("Referal", callback_data=str(REFERAL))],
        [InlineKeyboardButton("Settings", callback_data=str(GO_SETTINGS))],
        [InlineKeyboardButton("Support", url=SUPPORT_BOT_URL)],
        # [InlineKeyboardButton("Back", callback_data=str(BACK_LANG))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=log_in_mess, reply_markup=reply_markup)
    return FIRST


def select_pay(update: Update, context: CallbackContext) -> int:
    """Exchange menu"""
    query = update.callback_query
    userIDtmp = query.message.chat.id
    query.answer()

    if(query.data in currency_dict["pay_cur"]):
        up.set_pay_cur(
            userIDtmp, currency_dict["pay_cur"][query.data].get('name'))
        for key in currency_dict["pay_cur"]:
            if(key == query.data):
                currency_dict['pay_cur'][key]['status'] = emoji_fb['sel']
            else:
                currency_dict['pay_cur'][key]['status'] = emoji_fb['empty']

    exchange_mess = "Выберите валюту отправления:"
    # log_in_mess = langMessLib.exchange_mess(query, up)

    keyboard_global = []
    keyboard_row = []
    pay_cur_dict = currency_dict["pay_cur"]
    for key in pay_cur_dict:
        keyboard_row.append(InlineKeyboardButton(
            f"{pay_cur_dict[key].get('name')} {pay_cur_dict[key].get('status')}",
            callback_data=f"{pay_cur_dict[key].get('id')}"))
    keyboard_global.append(keyboard_row)

    keyboard_global.append([InlineKeyboardButton(
        "Confirm", callback_data=str(GO_INPUT_VALUE))])
    keyboard_global.append([InlineKeyboardButton(
        "Back", callback_data=str(GO_MAINPAGE))])

    reply_markup = InlineKeyboardMarkup(keyboard_global)
    query.edit_message_text(text=exchange_mess, reply_markup=reply_markup)
    return SECOND


def input_value(update: Update, context: CallbackContext) -> int:
    """keyboard input value to be exchanged"""
    query = update.callback_query
    userIDtmp = query.message.chat.id
    query.answer()
    input_mess = f"""Введите количество {up.get_pay_cur(userIDtmp)}:
        (только цифры nn, так же с плавающей запятой "nn.pp")
        """
    keyboard = [
        [InlineKeyboardButton("Change pay currency",
                              callback_data=str(GO_SELECT_PAY))]
    ]
    if(up.get_pay_cur(userIDtmp) == ""):
        input_mess = "Сначала выберите валюту для отправки: \"Select pay currency\""
        keyboard = [
            [InlineKeyboardButton("Select pay currency",
                                  callback_data=str(GO_SELECT_PAY))]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=input_mess, reply_markup=reply_markup)
    return SECOND


def input_confirm(update: Update, context: CallbackContext) -> int:
    """keyboard input value confirm"""
    # query = update.callback_query
    # query.answer()
    userIDtmp = update.message.chat.id
    print(update)
    up.set_value_cur(userIDtmp, update.message.text)
    keyboard = []
    if(up.get_pay_cur(userIDtmp) == ""):
        input_confirm_mess = "Сначала выберите валюту для отправки: \"Select pay currency\""
        keyboard = [
            [InlineKeyboardButton("Select pay currency",
                                  callback_data=str(GO_SELECT_PAY))]
        ]
    else:
        input_confirm_mess = f"Для обмена выбрано {update.message.text} {up.get_pay_cur(userIDtmp)}"
        keyboard = [
            [InlineKeyboardButton("Change pay currency",
                                  callback_data=str(GO_SELECT_PAY))],
            [InlineKeyboardButton("Select get currency",
                                  callback_data=str(GO_SELECT_GET))]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text=input_confirm_mess,
                              reply_markup=reply_markup)
    return SECOND


def select_get(update: Update, context: CallbackContext) -> int:
    """Exchange menu"""
    query = update.callback_query
    userIDtmp = query.message.chat.id
    query.answer()

    if query.data in currency_dict["get_cur"]:
        up.set_get_cur(
            userIDtmp, currency_dict["get_cur"][query.data].get('name'))
        for key in currency_dict["get_cur"]:
            if key == query.data:
                currency_dict['get_cur'][key]['status'] = emoji_fb['sel']
            else:
                currency_dict['get_cur'][key]['status'] = emoji_fb['empty']

    exchange_mess = "Выберите валюту получения:"
    keyboard_global = []
    keyboard_row = []
    get_cur_dict = currency_dict["get_cur"]
    for key in get_cur_dict:
        keyboard_row.append(InlineKeyboardButton(
            f"{get_cur_dict[key].get('name')} {get_cur_dict[key].get('status')}",
            callback_data=f"{get_cur_dict[key].get('id')}"))
    keyboard_global.append(keyboard_row)

    reply_markup = InlineKeyboardMarkup(keyboard_global)
    query.edit_message_text(text=exchange_mess, reply_markup=reply_markup)
    return SECOND


# SETTINGS:
def settings_page(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    mess = textwrap.dedent("""Меню настроек:""")
    keyboard = [
            [InlineKeyboardButton(
                "Requisites", callback_data=str(REQUISITES))],
            [InlineKeyboardButton(
                "Change language", callback_data=str(GO_LANGUAGE_SETTINGS))],
            [InlineKeyboardButton("Back", callback_data=str(GO_MAINPAGE))]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=mess, reply_markup=reply_markup)
    return FIRST


def language(update: Update, context: CallbackContext) -> int:
    """Change system language"""
    """Lead user to language in settings"""
    language_mess = textwrap.dedent(f"""
        Select language / Выбрать язык
        Selected / Выбранный : {up.get_lang(update.message.chat.id)}""")
    keyboard = [
        [InlineKeyboardButton("ENG", callback_data=str(LANG_ENG_SETTINGS)),
            InlineKeyboardButton("RUS", callback_data=str(LANG_RUS_SETTINGS))],
        [InlineKeyboardButton("Back", callback_data=str(GO_SETTINGS))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text=language_mess, reply_markup=reply_markup)
    return FIRST


def language_settings(update: Update, context: CallbackContext) -> int:
    """Change system language"""
    query = update.callback_query
    query.answer()
    userIDtmp = query.message.chat.id
    if(re.match(r'rus.*|eng.*', query.data)):
        lang_query = query.data
        up.set_lang(userIDtmp, lang_query.replace('_lang_settings', ''))
    language_mess = textwrap.dedent(f"""
        Select language / Выбрать язык
        Selected / Выбранный : {up.get_lang(userIDtmp)}""")
    keyboard = [
        [InlineKeyboardButton("ENG", callback_data=str(LANG_ENG_SETTINGS)),
            InlineKeyboardButton("RUS", callback_data=str(LANG_RUS_SETTINGS))],
        [InlineKeyboardButton("Back", callback_data=str(GO_SETTINGS))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=language_mess, reply_markup=reply_markup)
    return FIRST
#
#
# def support_menu(update: Update, context: CallbackContext) -> int:
#     """Short Support menu."""
#     """later add message handler for forwarding mess to support."""
#     """ Make possible conversate inside bot on this page."""
#     support_mess = langMessLib.support_mess(ep)
#     keyboard = [
#         [InlineKeyboardButton("Contact support", url=SUPPORT_BOT_URL)],
#         [InlineKeyboardButton("Back", callback_data=str(BACK_START))]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text(text=support_mess, reply_markup=reply_markup)
#     return FIRST
#
#
# def support_menu_over(update: Update, context: CallbackContext) -> int:
#     """Short Support menu."""
#     """later add message handler for forwarding mess to support."""
#     """ Make possible conversate inside bot on this page."""
#     query = update.callback_query
#     query.answer()
#     support_mess = langMessLib.support_mess(ep)
#     keyboard = [
#         [InlineKeyboardButton("Contact support", url=SUPPORT_BOT_URL)],
#         [InlineKeyboardButton("Back", callback_data=str(BACK_START))]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(text=support_mess, reply_markup=reply_markup)
#     return FIRST
#
#
# def share_group(update: Update, context: CallbackContext) -> None:
#     """Reached through the CHECK_THIS_OUT payload"""
#     bot = context.bot
#     url = helpers.create_deep_linked_url(bot.username, "so-cool")
#     welcome_mess = textwrap.dedent(f"""
#                     Hello, dear User!
#                     Check out da-hub exchange bot.
#                     Inside you find easyest way to
#                     buy, sell & exchange currencies!
#                     """)
#     keyboard = InlineKeyboardMarkup.from_button(
#         InlineKeyboardButton(text="Check this out", url=url)
#     )
#     update.message.reply_text(welcome_mess, reply_markup=keyboard)
#
# # def share_personal(update: Update, context: CallbackContext) -> None:
# #     bot = context.bot
# #     bot.send_message("dude")


def dict_extractor(keysList):
    compare_str = ""
    for i in keysList:
        compare_str += i + "|"
    print(compare_str)
    return compare_str


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token:
    updater = Updater(API_TOKEN)
    # Get the dispatcher to register handlers:
    dispatcher = updater.dispatcher
    #
    pay_query = dict_extractor(currency_dict['pay_cur'].keys())
    get_query = dict_extractor(currency_dict['get_cur'].keys())
    # numbers_query = ""
    # for key in numbers_keyboard:
    #     numbers_query += dict_extractor(numbers_keyboard[key].keys())

    # Register a deep-linking handler:
    # dispatcher.add_handler(
    #     CommandHandler("start", share_group, Filters.regex('check-this-out'))
    # )

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler('language', language),
            # CommandHandler('help', start),
            # CommandHandler('support', support_menu)
        ],
        states={
            FIRST: [
                CallbackQueryHandler(
                    language_over, pattern="^" + str(LOG_IN) + "$" + "|"
                    + "^" + str(LANG_ENG) + "$" + "|"
                    + "^" + str(LANG_RUS) + "$" + "|"
                    + str(GO_LANGUAGE)
                ),
                CallbackQueryHandler(
                    main_page, pattern="^" + str(GO_MAINPAGE) + "$"
                ),
                CallbackQueryHandler(
                    select_pay, pattern="^" + str(GO_SELECT_PAY) + "$" + "|"
                    + "^" + pay_query + "$"
                ),
                CallbackQueryHandler(
                    settings_page, pattern=str(GO_SETTINGS)
                ),
                CallbackQueryHandler(
                    language_settings, pattern="^" + \
                    str(GO_LANGUAGE_SETTINGS) + "$" + "|"
                    + "^" + str(LANG_ENG_SETTINGS) + "$" + "|"
                    + "^" + str(LANG_RUS_SETTINGS) + "$"
                ),

                # MessageHandler(
                #     Filters.regex('^([0-9]+.[0-9]+)$'), input_confirm
                # ),
                # CallbackQueryHandler(
                #     start_over, pattern='^' + str(BACK_START) + '$'
                # ),
                #
                # CallbackQueryHandler(
                #     support_menu_over, pattern=str(SUPPORT_MENU)
                # ),
            ],
            SECOND: [
                CallbackQueryHandler(
                    main_page, pattern="^" + str(GO_MAINPAGE) + "$"
                ),
                CallbackQueryHandler(
                    select_pay, pattern="^" + str(GO_SELECT_PAY) + "$" + "|"
                    + "^" + pay_query + "$"
                ),
                CallbackQueryHandler(
                    input_value, pattern="^" + str(GO_INPUT_VALUE) + "$"
                ),
                CallbackQueryHandler(
                    select_get, pattern="^" + str(GO_SELECT_GET) + "$" + "|"
                    + "^" + get_query + "$"
                ),
                MessageHandler(Filters.regex(
                    '^(([0-9]+\.[0-9]+)|[0-9]+)$'), input_confirm),
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
            CommandHandler('language', language),
            # CommandHandler('help', start),
            # CommandHandler('support', support_menu)

        ],
    )
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    # Start by webhook:
    # updater.start_webhook()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':

    up = UserPropeties()
    main()
