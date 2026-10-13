# “Mif yoki haqiqat?” Telegram-boti

15 savolli o'quv viktorinasi: har bir javobdan keyin to'g'ri/noto'g'ri holati va izoh ko'rsatiladi, yakunda ball va foiz hisoblanadi. Har bir foydalanuvchining natijasi alohida saqlanadi (bot jarayoni davomida).

## 1. Bot yaratish
1. Telegramda **@BotFather** ni oching.
2. `/newbot` yuboring va bot nomini kiriting.
3. Username tanlang (odatda `bot` bilan tugaydi).
4. BotFather bergan tokenni maxfiy saqlang. Uni hech kimga yubormang.

## 2. Kompyuterda ishga tushirish
Python 3.10 yoki undan yangiroq versiya o'rnating.

Terminal/Command Prompt'da loyiha papkasiga o'ting va bajaring:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Kutubxonalarni o'rnating:
```bash
pip install -r requirements.txt
```

`BOT_TOKEN` muhit o'zgaruvchisini o'rnating.

Windows PowerShell:
```powershell
$env:BOT_TOKEN="BOTFATHER_BERGAN_TOKEN"
python bot.py
```

macOS/Linux:
```bash
export BOT_TOKEN="BOTFATHER_BERGAN_TOKEN"
python bot.py
```

Terminalda “Bot ishga tushmoqda...” yozuvi ko'rinsa, Telegramda botni ochib `/start` yuboring.

## 3. Boshqalarga ulashish
Bot ishga tushganidan keyin:
- Bot ichida `/share` yuboring.
- Bot o'zining `https://t.me/BOT_USERNAME?start=quiz` havolasini beradi.
- Havolani Telegram guruhiga, kanalga yoki do'stlaringizga yuboring.
- Yangi foydalanuvchi havolani bosib **Start** tugmasini bosadi.

Botni 24/7 ishlatish uchun uni doim yoqilgan kompyuterda yoki Python qo'llab-quvvatlaydigan hosting/VPS xizmatida ishga tushiring. Oddiy kompyuter o'chsa, bot ham to'xtaydi.

## Muhim
- Bot tokenini ommaga chiqarmang va GitHub kabi ochiq joyga joylamang.
- Bu bot o'quv maqsadida. Tibbiy holatlarda shifokor tavsiyasi va mahalliy klinik protokollarga amal qiling.
- Natija joriy bot sessiyasida hisoblanadi; bu boshlang'ich versiyada doimiy reyting bazasi yo'q.
