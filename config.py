import os

# Telegram API credentials - get from environment variables with fallbacks
API_ID = int(os.getenv('TELEGRAM_API_ID', '28956309'))
API_HASH = os.getenv('TELEGRAM_API_HASH', '7b9e26b9fb9399e9adc12b40b3b5db48')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE', '+380630781027')
PASSWORD = os.getenv('TELEGRAM_PASSWORD', 'P190209r')
CHANNEL_ID = int(os.getenv('TELEGRAM_CHANNEL_ID', '-1002787265802'))

# Bot settings
SESSION_NAME = 'userbot_session'

# Keywords for heart reaction - всі варіанти ваших нікнеймів
KEYWORDS_FOR_HEART = [
    'кріхса', 'крихта', 'кочічка', "м'якенька", "м'якотіла", 
    'роксіс', 'рокса', 'рокстар', 'блейд', 'роксана',
    '@kpixca', 'kpixca', 'кпікса'
]

# Web dashboard settings
WEB_PORT = 5000
WEB_HOST = '0.0.0.0'
