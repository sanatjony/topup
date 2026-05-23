import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiohttp import web
import os

# 1. Telegram bot sozlamalari
API_TOKEN = os.environ.get('BOT_TOKEN', 'SIZNING_BOT_TOKENINGIZ')
WEB_APP_URL = os.environ.get('WEB_APP_URL', 'https://sizning-sayt-manzilingiz.railway.app')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# 2. Telegram bot qismi
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = InlineKeyboardMarkup()
    web_app_btn = InlineKeyboardButton(
        text="Jony PAY-ni ochish", 
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    markup.add(web_app_btn)
    await message.answer("Xush kelibsiz! Quyidagi tugma orqali Jony PAY tizimiga kiring:", reply_markup=markup)

# 3. Web App uchun HTML interfeys (HTML/CSS/JS)
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { font-family: sans-serif; background: #0b111a; color: white; margin: 0; padding-bottom: 70px; }
        .page { display: none; padding: 20px; }
        .active { display: block; }
        .nav-bar { position: fixed; bottom: 0; width: 100%; display: flex; justify-content: space-around; background: #161c26; padding: 10px 0; border-top: 1px solid #2d3440; }
        .nav-item { cursor: pointer; text-align: center; font-size: 12px; }
        .header { background: #161c26; padding: 20px; border-radius: 0 0 20px 20px; text-align: center; }
    </style>
</head>
<body>
    <div id="bosh-sahifa" class="page active">
        <div class="header"><h3>Jony PAY</h3></div>
        <p>Xush kelibsiz! O'yinlar ro'yxati:</p>
        <div style="background:#1e2735; padding:15px; border-radius:10px;">PUBG Mobile</div>
    </div>
    
    <div id="hamyon" class="page"><h3>Hamyon</h3><p>Balansingiz: 0 UZS</p></div>
    <div id="tarix" class="page"><h3>Tarix</h3><p>Hozircha tranzaksiyalar yo'q.</p></div>
    <div id="profil" class="page"><h3>Profil</h3><p>Foydalanuvchi: Sanatjony Aslonov</p></div>

    <div class="nav-bar">
        <div class="nav-item" onclick="showPage('bosh-sahifa')">🏠<br>Bosh sahifa</div>
        <div class="nav-item" onclick="showPage('hamyon')">💳<br>Hamyon</div>
        <div class="nav-item" onclick="showPage('tarix')">🕒<br>Tarix</div>
        <div class="nav-item" onclick="showPage('profil')">👤<br>Profil</div>
    </div>

    <script>
        function showPage(pageId) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById(pageId).classList.add('active');
        }
        Telegram.WebApp.ready();
    </script>
</body>
</html>
"""

# 4. Web server qismi
async def handle(request):
    return web.Response(text=HTML_CONTENT, content_type='text/html')

app = web.Application()
app.router.add_get('/', handle)

# 5. Bot va Serverni birga ishga tushirish
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    loop = asyncio.get_event_loop()
    loop.create_task(web._run_app(app, host='0.0.0.0', port=port))
    executor.start_polling(dp, skip_updates=True)
