import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import web

# Konfiguratsiya
API_TOKEN = os.environ.get('BOT_TOKEN')
WEB_APP_URL = os.environ.get('WEB_APP_URL')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Web App sahifalari uchun HTML
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #0b111a; color: white; font-family: sans-serif; margin: 0; padding-bottom: 70px; }
        .page { display: none; padding: 20px; }
        .active { display: block; }
        .nav-bar { position: fixed; bottom: 0; width: 100%; display: flex; justify-content: space-around; background: #161c26; padding: 10px 0; }
        .nav-item { cursor: pointer; text-align: center; }
    </style>
</head>
<body>
    <div id="bosh-sahifa" class="page active"><h3>Jony PAY</h3><p>PUBG Mobile UC</p></div>
    <div id="hamyon" class="page"><h3>Hamyon</h3><p>0 UZS</p></div>
    <div id="tarix" class="page"><h3>Tarix</h3><p>Bo'sh</p></div>
    <div id="profil" class="page"><h3>Profil</h3><p>Sanatjony Aslonov</p></div>

    <div class="nav-bar">
        <div class="nav-item" onclick="showPage('bosh-sahifa')">🏠<br>Asosiy</div>
        <div class="nav-item" onclick="showPage('hamyon')">💳<br>Hamyon</div>
        <div class="nav-item" onclick="showPage('tarix')">🕒<br>Tarix</div>
        <div class="nav-item" onclick="showPage('profil')">👤<br>Profil</div>
    </div>
    <script>
        function showPage(id) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById(id).classList.add('active');
        }
    </script>
</body>
</html>
"""

@dp.message(Command("start"))
async def start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Jony PAY-ni ochish", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer("Jony PAY tizimiga xush kelibsiz!", reply_markup=kb)

async def handle(request):
    return web.Response(text=HTML_CONTENT, content_type='text/html')

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080)))
    await site.start()
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
