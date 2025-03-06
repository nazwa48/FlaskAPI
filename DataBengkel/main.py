from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'RAHASIA'

@app.route('/')
def index():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM barang")
        items = cursor.fetchall()
    return render_template('index.html', items=items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return render_template('index.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        kode_barang = request.form['kode_barang']
        nama = request.form['nama']
        jumlah = request.form['jumlah']
        kondisi = request.form['kondisi']
        keterangan = request.form['keterangan']

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO barang (kode_barang, nama, jumlah, kondisi, keterangan) VALUES (?, ?, ?, ?, ?)",
                (kode_barang, nama, jumlah, kondisi, keterangan))
            conn.commit()

        return redirect(url_for('index'))

    return render_template('add_item.html')

@app.route('/api/bengkel', methods=['GET'])
def get_inventory():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM barang")
        items = cursor.fetchall()
    inventory_list = [
        {
            'id': item[0],
            'kode_barang': item[1],
            'nama': item[2],
            'jumlah': item[3],
            'kondisi': item[4],
            'keterangan': item[5]
        } for item in items
    ]
    return jsonify(inventory_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
