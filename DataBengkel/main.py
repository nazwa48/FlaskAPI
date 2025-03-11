from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'RAHASIA'

@app.before_request
def check_login():
    if 'username' not in session and request.endpoint not in ['login','get_inventory','static']:
        return redirect(url_for('login'))

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
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

        if user:
            stored_password = user[2]  # Mengambil kolom ke-2 (password) dalam hasil query
            if password == stored_password:
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash("Password salah!", "danger")
        else:
            flash("Username tidak ditemukan!", "danger")

    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return render_template('login.html')

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

# Edit barang
@app.route('/edit_item/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()

        if request.method == 'POST':
            kode_barang = request.form['kode_barang']
            nama = request.form['nama']
            jumlah = request.form['jumlah']
            kondisi = request.form['kondisi']
            keterangan = request.form['keterangan']

            cursor.execute(
                "UPDATE barang SET kode_barang = ?, nama = ?, jumlah = ?, kondisi = ?, keterangan = ? WHERE id = ?",
                (kode_barang, nama, jumlah, kondisi, keterangan, id))
            conn.commit()

            return redirect(url_for('index'))

        cursor.execute("SELECT * FROM barang WHERE id = ?", (id,))
        item = cursor.fetchone()

    return render_template('edit_item.html', item=item)

# Hapus barang
@app.route('/delete_item/<int:id>')
def delete_item(id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM barang WHERE id = ?", (id,))
        conn.commit()

    return redirect(url_for('index'))


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
