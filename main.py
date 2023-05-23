from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters

from getmusic import YouTubeMusic
from keepalive import keep_alive
from asyncio import sleep
from loguru import logger

from random import choice
from os import environ

# Configure logging
logger.add("logs.log", format="{time} {level} {message}",
           level="INFO", rotation="10 KB", compression="zip")

# Initialize bot and dispatcher
bot = Bot(environ["API_TOKEN"])
dp = Dispatcher(bot)


async def on_startup(_):
    print("Гамарджоба друг мой, можешь отдохнуть, я бот запустил.")


class Secret:
    channel_user = environ["CHANNEL_USER"]
    channel_music = environ["CHANNEL_MUSIC"]


class Text:
    caption = (
            "<em>Столько: {0:,d} людей прослушали</em>.\n"
            "<em>Дата публикации: {1}г</em>."
            )
    description = (
            "Привет, <b>{0}</b>🤚\n\n"
            "Я помогу найти аудио в YouTube Music и по возможности "
            "отправлю тебе его!\n"
            "  • Просто перешли мне музыкальный клип с youtube.\n"
            "  • Я ищу только оригиналы треков, без фанатских "
            "ремиксов и записи с диктофона!\n"
            "  • Формат треков — M4A AAC 128 Kbps. Это оригинальный "
            "формат аудио на YouTube.\n"
            "  • Обложки альбомов прилагаются!\n"
            "Нужен свой личный бот с блекджеками и девушками?\n"
            "Пиши - @mac_loves\n\n"
            "--------------------\n"
            "<em>Сообщение автоматически удалится</em>"
            )
    data_user = (
            "{0} - ID пользователя\n"
            "{1} - Имя пользователя\n"
            "{2} - Фамилия или псевдоним пользователя\n"
            "@{3} - Никнейм пользователя"
            )
    legal = (
            "Я создал BotMusic с идеей, что должен существовать легальный "
            "инструмент для записи потоковой передачи в Интернете, который "
            "был бы чистым, простым и не содержал спама. Согласно EFF.org, "
            "«в законе ясно, что простоепредоставление общественности "
            "инструмента для копирования цифровых носителей не влечет за "
            "собой ответственности за авторские права».\n\n"
            "--------------------\n"
            "<em>Сообщение автоматически удалится</em>"
            )
    own_bot = (
            "<em><b>Хочешь своего бота?</b></em>\n"
            "Пиши - @mac_loves\n\n"
            "--------------------\n"
            "<em>Сообщение автоматически удалится</em>"
            )
    answer_for_magicball = [
            'Бесспорно', 'Мне кажется - да', 'Пока неясно, попробуй снова',
            'Даже не думай', 'Предрешено', 'Вероятнее всего', 'Спроси позже',
            'Мой ответ - нет', 'Никаких сомнений', 'Хорошие перспективы',
            'Лучше не рассказывать', 'По моим данным - нет', 'Определённо да',
            'Знаки говорят - да', 'Сейчас нельзя предсказать',
            'Перспективы не очень хорошие', 'Можешь быть уверен в этом', 'Да',
            'Сконцентрируйся и спроси опять', 'Весьма сомнительно'
            ]


class Buttons:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=False)

    kb1 = types.KeyboardButton('Помощь🚒')
    kb2 = types.KeyboardButton('Легально?⚠')
    kb3 = types.KeyboardButton('Свой бот🤖')
    kb4 = types.KeyboardButton('Шар предсказания🎱')
    kb.add(kb4).add(kb1, kb2, kb3)


@dp.message_handler(commands=["info", "start"])
async def start_commands(message: types.Message) -> None:
    await message.delete()

    answer = await message.answer(
            text=Text.description.format(message.from_user.first_name),
            parse_mode="html", reply_markup=Buttons.kb
            )
    if message.text == "/start":
        await bot.send_message(
                chat_id=Secret.channel_user,
                text=Text.data_user.format(message.from_user.id,
                                           message.from_user.first_name,
                                           message.from_user.last_name,
                                           message.from_user.username)
                )
    await sleep(180)

    # На случай, если пользователь удалит раньше сообщение
    try:
        await bot.delete_message(message.chat.id, answer.message_id)
    except:
        pass 
    


@dp.message_handler(filters.Text(equals="Помощь🚒"))
async def helper(message: types.Message) -> None:
    await start_commands(message)


@dp.message_handler(filters.Text(equals="Легально?⚠"))
async def legal(message: types.Message) -> None:
    await message.delete()

    answer = await message.answer(text=Text.legal, parse_mode="html")
    await sleep(30)

    # На случай, если пользователь удалит раньше сообщение
    try:
        await bot.delete_message(message.chat.id, answer.message_id)
    except:
        pass


@dp.message_handler(filters.Text(equals="Свой бот🤖"))
async def own_bot(message: types.Message) -> None:
    await message.delete()

    answer = await message.answer(text=Text.own_bot, parse_mode="html")
    await sleep(30)

    # На случай, если пользователь удалит раньше сообщение
    try:
        await bot.delete_message(message.chat.id, answer.message_id)
    except:
        pass


@dp.message_handler(filters.Text(equals="Шар предсказания🎱"))
async def magic_ball(message: types.Message) -> None:
    await message.delete()

    answer = await message.answer(text=choice(Text.answer_for_magicball))
    await sleep(7)

    # На случай, если пользователь удалит раньше сообщение
    try:
        await bot.delete_message(message.chat.id, answer.message_id)
    except:
        pass


@dp.message_handler(filters.Text(startswith=("https://youtu.be/",
                                             "https://www.youtube.com/"),
                                 ignore_case=True))
async def main(message: types.Message) -> None:
    await message.delete()

    answer = await message.answer("<em><b>Проверяю..</b></em>",
                                  parse_mode="html")
    audio = YouTubeMusic(message.text)

    if audio.response_valid == True:
        await answer.edit_text("<em><b>all Good! - Скачиваю музыку.</b></em>",
                               parse_mode="html")
        music_answer = await message.answer_audio(
                audio=audio.get_music(),
                caption=Text.caption.format(audio.views, audio.pub),
                thumb=types.InputFile.from_url(audio.thumb),
                parse_mode="html",
                title=audio.title
                )
        await bot.forward_message(
                chat_id=Secret.channel_music,
                from_chat_id=message.chat.id,
                message_id=music_answer.message_id
                )
    else:
        logger.error(audio.response_valid)
        await answer.edit_text(f"<em><b>No good.\nОшибка: "
                               f"{audio.response_valid.args[0]}</b></em>",
                               parse_mode="html")
        await sleep(10)

    # На случай, если пользователь удалит раньше сообщение
    try:
        await bot.delete_message(message.chat.id, answer.message_id)
    except:
        pass  


if __name__ == "__main__":
    keep_alive()
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
