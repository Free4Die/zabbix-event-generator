from flask import Flask, render_template, request, redirect
import subprocess
import os

app = Flask(__name__)

# Список твоих метрик (item_key: description)
METRICS = {
    "app.error.critical": "Критическая ошибка приложения",
    "db.connection.timeout": "Тайм-аут подключения к БД",
    "disk.space.warning": "Нехватка места на разделе /var/log",
    "service.status.nginx": "Статус службы Nginx",
    "web.requests.count": "Колличество запросов на сайт",
    "mem.usage.percent": "Процент используемой оперативной памяти",
    "auth.failed.attempts": "Превышено колличество неудачных авторизаций"
}

ZABBIX_SERVER = os.getenv("ZABBIX_SERVER", "127.0.0.1")
HOST_NAME = os.getenv("HOST_NAME", "Zabbix-Agent-Lab")

def send_to_zabbix(key, value):
    cmd = ["zabbix_sender", "-z", ZABBIX_SERVER, "-s", HOST_NAME, "-k", key, "-o", str(value)]
    try:
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html', metrics=METRICS, z_server=ZABBIX_SERVER, host=HOST_NAME)

@app.route('/send', methods=['POST'])
def send():
    key = request.form.get('key')
    value = request.form.get('value')
    if key and value:
        send_to_zabbix(key, value)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
