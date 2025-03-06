import sqlite3

def create_tabel():
    # Koneksi ke database (jika tidak ada, akan dibuat otomatis)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Perintah untuk membuat tabel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS barang (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode_barang TEXT UNIQUE NOT NULL,
            nama TEXT NOT NULL,
            jumlah INTEGER NOT NULL DEFAULT 0,
            kondisi TEXT NOT NULL,
            keterangan TEXT
        )
    ''')

    # Simpan perubahan dan tutup koneksi
    conn.commit()
    conn.close()

    print("Tabel berhasil dibuat!")

def create_tabel_user():
    # Koneksi ke database (jika tidak ada, akan dibuat otomatis)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Perintah untuk membuat tabel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",("nz", "12345678"))
    # Simpan perubahan dan tutup koneksi
    conn.commit()
    conn.close()

    print("Tabel berhasil dibuat!")

create_tabel_user()