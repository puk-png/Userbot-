from flask import Flask, render_template, jsonify
import threading
import time
from config import WEB_HOST, WEB_PORT

app = Flask(__name__)
bot_status_ref = None

@app.route('/')
def dashboard():
    """Головна сторінка дашборду"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """API endpoint для отримання статусу бота"""
    if bot_status_ref is None:
        return jsonify({
            'error': 'Bot not initialized',
            'is_running': False
        })
    
    return jsonify({
        'is_running': bot_status_ref.is_running,
        'commands_processed': bot_status_ref.commands_processed,
        'reactions_sent': bot_status_ref.reactions_sent,
        'messages_processed': bot_status_ref.messages_processed,
        'last_error': bot_status_ref.last_error,
        'uptime': time.time() - start_time if bot_status_ref.is_running else 0
    })

@app.route('/api/clear_error')
def clear_error():
    """Очистити останню помилку"""
    if bot_status_ref:
        bot_status_ref.last_error = None
    return jsonify({'success': True})

start_time = time.time()

def start_web_server(status):
    """Запускає веб-сервер"""
    global bot_status_ref, start_time
    bot_status_ref = status
    start_time = time.time()
    
    try:
        app.run(host=WEB_HOST, port=WEB_PORT, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Помилка запуску веб-сервера: {e}")
