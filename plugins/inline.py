import logging
from pyrogram import Client, emoji, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument

from utils import get_search_results, is_subscribed
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION

logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME


@Client.on_inline_query(filters.user(AUTH_USERS) if AUTH_USERS else None)
async def answer(bot, query):
    """Show search results for given inline query"""

    if AUTH_CHANNEL and not await is_subscribed(bot, query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='You have to subscribe my channel to use the bot',
                           switch_pm_parameter="subscribe")
        return

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    reply_markup = get_reply_markup(query=string)
    files, next_offset = await get_search_results(string,
                                                  file_type=file_type,
                                                  max_results=10,
                                                  offset=offset)

    for file in files:
        title=file.file_name
        size=file.file_size
        f_caption=file.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
            except Exception as e:
                print(e)
                f_caption=f_caption
        if f_caption is None:
            f_caption = f"{file.file_name}"
        results.append(
            InlineQueryResultCachedDocument(
                title=file.file_name,
                file_id=file.file_id,
                caption=f_caption,
                description=f'Size: {get_size(file.file_size)}\nType: {file.file_type}',
                reply_markup=reply_markup))

    if results:
        switch_pm_text = f"{emoji.FILE_FOLDER} Results"
        if string:
            switch_pm_text += f" for {string}"

        await query.answer(results=results,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
    else:

        switch_pm_text = f'{emoji.CROSS_MARK} No results'
        if string:
            switch_pm_text += f' for "{string}"'

        await query.answer(results=[],
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")


def get_reply_markup(query):
    buttons = [
        [
            InlineKeyboardButton('Search again', switch_inline_query_current_chat=query),
            InlineKeyboardButton('Share Me', url='https://t.me/share/url?url=%E0%B4%B8%E0%B4%BF%E0%B4%A8%E0%B4%BF%E0%B4%AE%E0%B4%95%E0%B4%B3%E0%B5%81%E0%B4%82%20%E0%B4%AA%E0%B5%81%E0%B4%B8%E0%B5%8D%E0%B4%A4%E0%B4%95%E0%B4%99%E0%B5%8D%E0%B4%99%E0%B4%B3%E0%B5%81%E0%B4%82%20%E0%B4%B8%E0%B5%97%E0%B4%9C%E0%B4%A8%E0%B5%8D%E0%B4%AF%E0%B4%AE%E0%B4%BE%E0%B4%AF%E0%B4%BF%20%E0%B4%A1%E0%B5%97%E0%B5%BA%E0%B4%B2%E0%B5%8B%E0%B4%A1%E0%B5%8D%20%E0%B4%9A%E0%B5%86%E0%B4%AF%E0%B5%8D%E0%B4%AF%E0%B5%81%E0%B4%B5%E0%B4%BE%E0%B5%BB%20%E0%B4%92%E0%B4%B0%E0%B5%81%20%E0%B4%B8%E0%B4%82%E0%B4%B5%E0%B4%BF%E0%B4%A7%E0%B4%BE%E0%B4%A8%E0%B4%82.%0A%E0%B4%9E%E0%B4%BE%E0%B5%BB%20%E0%B4%87%E0%B4%A4%E0%B5%8D%20%E0%B4%89%E0%B4%AA%E0%B4%AF%E0%B5%8B%E0%B4%97%E0%B4%BF%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%81%E0%B4%A8%E0%B5%8D%E0%B4%A8%E0%B5%81.%20%0A%E0%B4%B5%E0%B4%B3%E0%B4%B0%E0%B5%86%E0%B4%AF%E0%B4%A7%E0%B4%BF%E0%B4%95%E0%B4%82%20%E0%B4%89%E0%B4%AA%E0%B4%95%E0%B4%BE%E0%B4%B0%E0%B4%AA%E0%B5%8D%E0%B4%B0%E0%B4%A6%E0%B4%AE%E0%B4%BE%E0%B4%A3%E0%B5%8D%20%E0%B4%88%20%E0%B4%B8%E0%B4%82%E0%B4%B5%E0%B4%BF%E0%B4%A7%E0%B4%BE%E0%B4%A8%E0%B4%82.%20%0A%0A%E0%B4%8E%E0%B4%A8%E0%B5%8D%E0%B4%A4%E0%B5%86%E0%B4%99%E0%B5%8D%E0%B4%95%E0%B4%BF%E0%B4%B2%E0%B5%81%E0%B4%82%20%E0%B4%B8%E0%B4%82%E0%B4%B6%E0%B4%AF%E0%B4%82%20%E0%B4%89%E0%B4%A3%E0%B5%8D%E0%B4%9F%E0%B5%86%E0%B4%99%E0%B5%8D%E0%B4%95%E0%B4%BF%E0%B5%BD%20%5B%E0%B4%87%E0%B4%A4%E0%B5%8D%20%E0%B4%B6%E0%B5%8D%E0%B4%B0%E0%B4%A6%E0%B5%8D%E0%B4%A7%E0%B4%BF%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%81%E0%B4%95%5D%28https%3A//t.me/Douglas_Works/25%29%0A%0A%E0%B4%87%E0%B4%AA%E0%B5%8D%E0%B4%AA%E0%B5%8B%E0%B5%BE%E0%B4%A4%E0%B5%8D%E0%B4%A4%E0%B4%A8%E0%B5%8D%E0%B4%A8%E0%B5%86%20%E0%B4%89%E0%B4%AA%E0%B4%AF%E0%B5%8B%E0%B4%97%E0%B4%BF%E0%B4%9A%E0%B5%8D%E0%B4%9A%E0%B5%81%E0%B4%A8%E0%B5%8B%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%82%20%3A-%20%5B%F0%9F%91%89CLICK%20HERE%F0%9F%91%88%5D%28https%3A//t.me/Kilipoyabot%29')
        ]
        ]
    return InlineKeyboardMarkup(buttons)


def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

