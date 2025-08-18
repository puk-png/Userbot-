# Telegram Userbot - Інструкції з встановлення

## Системні вимоги
- Python 3.11+
- ffmpeg (для обробки голосових повідомлень)

## Встановлення

### 1. Розпакуйте архів
```bash
tar -xzf telegram-userbot-full.tar.gz
cd telegram-userbot/
```

### 2. Встановіть залежності
```bash
pip install telethon speechrecognition pydub requests flask
```

### 3. Встановіть ffmpeg
**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Завантажте з https://ffmpeg.org/download.html

### 4. Налаштуйте API ключі
Відредагуйте файл `config.py` або встановіть змінні оточення:
- `TELEGRAM_API_ID` - ваш API ID з my.telegram.org
- `TELEGRAM_API_HASH` - ваш API Hash з my.telegram.org  
- `TELEGRAM_PHONE` - ваш номер телефону
- `TELEGRAM_PASSWORD` - пароль двофакторної автентифікації (якщо є)
- `TELEGRAM_CHANNEL_ID` - ID каналу для команди /random

### 5. Перша авторизація
```bash
python setup_auth.py
```
Введіть код підтвердження з SMS/Telegram

### 6. Запуск бота
```bash
python main.py
```

Або для простого запуску після авторизації:
```bash
python run_bot.py
```

## Функції бота

### Команди:
- `/gayporn` або `/random` - випадкове повідомлення з каналу
- `/voice` (у відповіді на голосове) - конвертація голосу в текст
- `/status` - показати статус бота

### Автоматичні функції:
- Реакція ❤️‍🔥 на ключові слова
- Відповідь "Героям слава!" на "Слава Україні" 
- Відповідь "Путін хуйло" на згадування "Путін"

### Веб-дашборд:
Доступний на http://localhost:5000 для моніторингу статусу

## Файли проєкту
- `main.py` - Основний файл запуску з авторизацією
- `run_bot.py` - Простий запуск після авторизації
- `setup_auth.py` - Скрипт першої авторизації
- `bot_handlers.py` - Обробники команд та автоматичних функцій
- `config.py` - Конфігурація та налаштування
- `web_dashboard.py` - Flask веб-сервер
- `templates/` - HTML шаблони для веб-інтерфейсу
- `static/` - CSS та JavaScript файли

Створено: 18 серпня 2025