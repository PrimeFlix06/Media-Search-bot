#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from utils import get_filter_results, get_file_details, is_subscribed, get_poster
BUTTONS = {}
BOT = {}
@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**എൻ്റെ ചാനലിൽ ജോയിൻ ചെയ്താലേ എന്നെ ഉപയോഗിക്കാൻ കഴിയൂ!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🥰എൻ്റെ ചാനൽ🥰", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAADBQADgQMAAhr_EVTvzu4UxRkTvQI')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>🎬 Film/Series : {search}

🌟 IMDB Rating : 7.5/10

🎭 Genres: Document, 🔪 Drama, Thriller, Comedy</b>", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(f"<b>🎬 Film/Series : {search}

🌟 IMDB Rating : 7.5/10

🎭 Genres: Document, 🔪 Drama, Thriller, Comedy</b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>🎬 Film/Series : {search}

🌟 IMDB Rating : 7.5/10

🎭 Genres: Document, 🔪 Drama, Thriller, Comedy</b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>🎬 Film/Series : {search}

🌟 IMDB Rating : 7.5/10

🎭 Genres: Document, 🔪 Drama, Thriller, Comedy</b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('Update Channel', url='https://t.me/Douglas_Works'),
                    InlineKeyboardButton('Source Code', url='https://t.me/Uvva_IppoKittum_Nokkiyirunno/5')
                ]
                ]
            await query.message.edit(text="<b>Developer : <a href='https://t.me/Username_Idarilla'>DOUGLAS</a>\nLanguage : <code>MALAYALAM</code>\nBIG FAN : <a href='https://telegra.ph/file/40274dfccb4ada872eec7.jpg'</a>\nSource Code : <a href='https://t.me/Uvva_IppoKittum_Nokkiyirunno/5'>Click here</a>\nChannel : <a href='https://t.me/cinema_club_channel'>സിനിമ ക്ലബ്</a> </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)



        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('Share Me', url='https://t.me/share/url?url=%E0%B4%B8%E0%B4%BF%E0%B4%A8%E0%B4%BF%E0%B4%AE%E0%B4%95%E0%B4%B3%E0%B5%81%E0%B4%82%20%E0%B4%AA%E0%B5%81%E0%B4%B8%E0%B5%8D%E0%B4%A4%E0%B4%95%E0%B4%99%E0%B5%8D%E0%B4%99%E0%B4%B3%E0%B5%81%E0%B4%82%20%E0%B4%B8%E0%B5%97%E0%B4%9C%E0%B4%A8%E0%B5%8D%E0%B4%AF%E0%B4%AE%E0%B4%BE%E0%B4%AF%E0%B4%BF%20%E0%B4%A1%E0%B5%97%E0%B5%BA%E0%B4%B2%E0%B5%8B%E0%B4%A1%E0%B5%8D%20%E0%B4%9A%E0%B5%86%E0%B4%AF%E0%B5%8D%E0%B4%AF%E0%B5%81%E0%B4%B5%E0%B4%BE%E0%B5%BB%20%E0%B4%92%E0%B4%B0%E0%B5%81%20%E0%B4%B8%E0%B4%82%E0%B4%B5%E0%B4%BF%E0%B4%A7%E0%B4%BE%E0%B4%A8%E0%B4%82.%0A%E0%B4%9E%E0%B4%BE%E0%B5%BB%20%E0%B4%87%E0%B4%A4%E0%B5%8D%20%E0%B4%89%E0%B4%AA%E0%B4%AF%E0%B5%8B%E0%B4%97%E0%B4%BF%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%81%E0%B4%A8%E0%B5%8D%E0%B4%A8%E0%B5%81.%20%0A%E0%B4%B5%E0%B4%B3%E0%B4%B0%E0%B5%86%E0%B4%AF%E0%B4%A7%E0%B4%BF%E0%B4%95%E0%B4%82%20%E0%B4%89%E0%B4%AA%E0%B4%95%E0%B4%BE%E0%B4%B0%E0%B4%AA%E0%B5%8D%E0%B4%B0%E0%B4%A6%E0%B4%AE%E0%B4%BE%E0%B4%A3%E0%B5%8D%20%E0%B4%88%20%E0%B4%B8%E0%B4%82%E0%B4%B5%E0%B4%BF%E0%B4%A7%E0%B4%BE%E0%B4%A8%E0%B4%82.%20%0A%0A%E0%B4%8E%E0%B4%A8%E0%B5%8D%E0%B4%A4%E0%B5%86%E0%B4%99%E0%B5%8D%E0%B4%95%E0%B4%BF%E0%B4%B2%E0%B5%81%E0%B4%82%20%E0%B4%B8%E0%B4%82%E0%B4%B6%E0%B4%AF%E0%B4%82%20%E0%B4%89%E0%B4%A3%E0%B5%8D%E0%B4%9F%E0%B5%86%E0%B4%99%E0%B5%8D%E0%B4%95%E0%B4%BF%E0%B5%BD%20%5B%E0%B4%87%E0%B4%A4%E0%B5%8D%20%E0%B4%B6%E0%B5%8D%E0%B4%B0%E0%B4%A6%E0%B5%8D%E0%B4%A7%E0%B4%BF%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%81%E0%B4%95%5D%28https%3A//t.me/Douglas_Works/25%29%0A%0A%E0%B4%87%E0%B4%AA%E0%B5%8D%E0%B4%AA%E0%B5%8B%E0%B5%BE%E0%B4%A4%E0%B5%8D%E0%B4%A4%E0%B4%A8%E0%B5%8D%E0%B4%A8%E0%B5%86%20%E0%B4%89%E0%B4%AA%E0%B4%AF%E0%B5%8B%E0%B4%97%E0%B4%BF%E0%B4%9A%E0%B5%8D%E0%B4%9A%E0%B5%81%E0%B4%A8%E0%B5%8B%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%82%20%3A-%20%5B%F0%9F%91%89CLICK%20HERE%F0%9F%91%88%5D%28https%3A//t.me/Kilipoyabot%29'),
                        InlineKeyboardButton('Update Channel', url='https://t.me/Douglas_Works')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('Share Me', url='https://t.me/share/url?url=%E0%B4%B8%E0%B4%BF%E0%B4%A8%E0%B4%BF%E0%B4%AE%E0%B4%95%E0%B4%B3%E0%B5%81%E0%B4%82%20%E0%B4%AA%E0%B5%81%E0%B4%B8%E0%B5%8D%E0%B4%A4%E0%B4%95%E0%B4%99%E0%B5%8D%E0%B4%99%E0%B4%B3%E0%B5%81%E0%B4%82%20%E0%B4%B8%E0%B5%97%E0%B4%9C%E0%B4%A8%E0%B5%8D%E0%B4%AF%E0%B4%AE%E0%B4%BE%E0%B4%AF%E0%B4%BF%20%E0%B4%A1%E0%B5%97%E0%B5%BA%E0%B4%B2%E0%B5%8B%E0%B4%A1%E0%B5%8D%20%E0%B4%9A%E0%B5%86%E0%B4%AF%E0%B5%8D%E0%B4%AF%E0%B5%81%E0%B4%B5%E0%B4%BE%E0%B5%BB%20%E0%B4%92%E0%B4%B0%E0%B5%81%20%E0%B4%B8%E0%B4%82%E0%B4%B5%E0%B4%BF%E0%B4%A7%E0%B4%BE%E0%B4%A8%E0%B4%82.%0A%E0%B4%9E%E0%B4%BE%E0%B5%BB%20%E0%B4%87%E0%B4%A4%E0%B5%8D%20%E0%B4%89%E0%B4%AA%E0%B4%AF%E0%B5%8B%E0%B4%97%E0%B4%BF%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%81%E0%B4%A8%E0%B5%8D%E0%B4%A8%E0%B5%81.%20%0A%E0%B4%B5%E0%B4%B3%E0%B4%B0%E0%B5%86%E0%B4%AF%E0%B4%A7%E0%B4%BF%E0%B4%95%E0%B4%82%20%E0%B4%89%E0%B4%AA%E0%B4%95%E0%B4%BE%E0%B4%B0%E0%B4%AA%E0%B5%8D%E0%B4%B0%E0%B4%A6%E0%B4%AE%E0%B4%BE%E0%B4%A3%E0%B5%8D%20%E0%B4%88%20%E0%B4%B8%E0%B4%82%E0%B4%B5%E0%B4%BF%E0%B4%A7%E0%B4%BE%E0%B4%A8%E0%B4%82.%20%0A%0A%E0%B4%8E%E0%B4%A8%E0%B5%8D%E0%B4%A4%E0%B5%86%E0%B4%99%E0%B5%8D%E0%B4%95%E0%B4%BF%E0%B4%B2%E0%B5%81%E0%B4%82%20%E0%B4%B8%E0%B4%82%E0%B4%B6%E0%B4%AF%E0%B4%82%20%E0%B4%89%E0%B4%A3%E0%B5%8D%E0%B4%9F%E0%B5%86%E0%B4%99%E0%B5%8D%E0%B4%95%E0%B4%BF%E0%B5%BD%20%5B%E0%B4%87%E0%B4%A4%E0%B5%8D%20%E0%B4%B6%E0%B5%8D%E0%B4%B0%E0%B4%A6%E0%B5%8D%E0%B4%A7%E0%B4%BF%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%81%E0%B4%95%5D%28https%3A//t.me/Douglas_Works/25%29%0A%0A%E0%B4%87%E0%B4%AA%E0%B5%8D%E0%B4%AA%E0%B5%8B%E0%B5%BE%E0%B4%A4%E0%B5%8D%E0%B4%A4%E0%B4%A8%E0%B5%8D%E0%B4%A8%E0%B5%86%20%E0%B4%89%E0%B4%AA%E0%B4%AF%E0%B5%8B%E0%B4%97%E0%B4%BF%E0%B4%9A%E0%B5%8D%E0%B4%9A%E0%B5%81%E0%B4%A8%E0%B5%8B%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%82%20%3A-%20%5B%F0%9F%91%89CLICK%20HERE%F0%9F%91%88%5D%28https%3A//t.me/Kilipoyabot%29'),
                        InlineKeyboardButton('Update Channel', url='https://t.me/Douglas_Works')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("നീ ഏതാ? നിനക്ക് വേണങ്കിൽ നീ തന്നെ ചോദിക്കണം!",show_alert=True)
