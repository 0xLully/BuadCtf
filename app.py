from flask import Flask, request, render_template_string
import sqlite3

# إنشاء تطبيق Flask
app = Flask(__name__)

# تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    c.execute('INSERT INTO users (username, password) VALUES ("admin", "password123")')
    conn.commit()
    conn.close()

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template_string("""
        <h1>تسجيل الدخول</h1>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="اسم المستخدم"><br>
            <input type="password" name="password" placeholder="كلمة المرور"><br>
            <input type="submit" value="تسجيل الدخول">
        </form>
        <!-- Flag 1: FLAG{W3lc0m3_T0_CTF} -->
    """)

# تسجيل الدخول
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # ثغرة SQL Injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    c.execute(query)
    result = c.fetchone()

    conn.close()

    if result:
        return "تم تسجيل الدخول بنجاح! Flag 2: FLAG{SQLi_1s_Fun}"
    else:
        return "فشل في تسجيل الدخول"

# صفحة سرية تحتوي على Flag
@app.route('/secret')
def secret():
    return "Flag 3: FLAG{S3cr3t_P4g3}"

# صفحة تحتوي على معلومات إضافية
@app.route('/info')
def info():
    return """
        <h1>معلومات إضافية</h1>
        <p>هذه صفحة تحتوي على معلومات غير مهمة.</p>
        <!-- Flag 4: FLAG{H1dd3n_1n_H7ML} -->
    """

# تشغيل التطبيق
if __name__ == '__main__':
    init_db()
    app.run(debug=True)