from bot import bot, dp
from keyboards import ListOfButtons
from filters import *
from post import *
from aiogram import md, types
from aiogram.utils.exceptions import MessageNotModified


def get_keyboard() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for post_id, post in POSTS.items():
        markup.add(
            types.InlineKeyboardButton(
                post['title'],
                callback_data=posts_cb.new(id=post_id, action='view')),
        )
    return markup


def format_post(post_id: str, post: dict) -> (str, types.InlineKeyboardMarkup):
    text = md.text(
        md.hbold(post['title']),
        md.quote_html(post['body'])
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Geri', callback_data=posts_cb.new(id='-', action='list')))
    return text, markup


@dp.message_handler(Button('Kategoriler'))
async def btnl(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Lütfen kategori seçiniz', reply_markup=get_keyboard())


@dp.callback_query_handler(posts_cb.filter(action='list'))
async def query_show_list(query: types.CallbackQuery):
    await query.message.edit_text('Lütfen kategori seçiniz', reply_markup=get_keyboard())


@dp.callback_query_handler(posts_cb.filter(action='view'))
async def query_view(query: types.CallbackQuery, callback_data: dict):
    post_id = callback_data['id']

    post = POSTS.get(post_id, None)
    if not post:
        return await query.answer('Post Bulunamadı')

    text, markup = format_post(post_id, post)
    await query.message.edit_text(text, reply_markup=markup)


@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    return True


@dp.message_handler(commands="start")
async def keyboards(message: Message):
    chat_id = message.chat.id
    keyboard = ListOfButtons(
        text=['Kategoriler', 'Sohbet', 'İletişim'],
        align=[1, 2]
    ).reply_keyboard
    await bot.send_document(chat_id,("CAADBAADJwADhEa6Gq0m-NvEsdVGFgQ"), reply_markup=keyboard),
    await bot.send_message(chat_id, ("Merhaba"), reply_markup=keyboard)

