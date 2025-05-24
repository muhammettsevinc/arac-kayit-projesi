from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_NAME = "database.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marka_model TEXT NOT NULL,
                yakit_turu TEXT NOT NULL,
                sanziman_turu TEXT NOT NULL,
                kasa_turu TEXT NOT NULL,
                kilometre INTEGER NOT NULL,
                yil INTEGER NOT NULL,
                plaka TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        marka_model = request.form['marka_model']
        yakit_turu = request.form['yakit_turu']
        sanziman_turu = request.form['sanziman_turu']
        kasa_turu = request.form['kasa_turu']
        kilometre = int(request.form['kilometre'])
        yil = int(request.form['yil'])
        plaka = request.form['plaka']

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO cars (marka_model, yakit_turu, sanziman_turu, kasa_turu, kilometre, yil, plaka)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (marka_model, yakit_turu, sanziman_turu, kasa_turu, kilometre, yil, plaka))
            conn.commit()

        return redirect(url_for('list_cars'))

    return render_template('add_car.html')

@app.route('/list')
def list_cars():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars')
        cars = cursor.fetchall()

    return render_template('list_cars.html', cars=cars)

@app.route('/delete/<int:id>')
def delete_car(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cars WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('list_cars'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_car(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        if request.method == 'POST':
            marka_model = request.form['marka_model']
            yakit_turu = request.form['yakit_turu']
            sanziman_turu = request.form['sanziman_turu']
            kasa_turu = request.form['kasa_turu']
            kilometre = int(request.form['kilometre'])
            yil = int(request.form['yil'])
            plaka = request.form['plaka']

            cursor.execute('''
                UPDATE cars
                SET marka_model = ?, yakit_turu = ?, sanziman_turu = ?, kasa_turu = ?, kilometre = ?, yil = ?, plaka = ?
                WHERE id = ?
            ''', (marka_model, yakit_turu, sanziman_turu, kasa_turu, kilometre, yil, plaka, id))
            conn.commit()
            return redirect(url_for('list_cars'))

        cursor.execute('SELECT * FROM cars WHERE id = ?', (id,))
        car = cursor.fetchone()

    return render_template('update_car.html', car=car)

if __name__ == '__main__':
    app.run(debug=True)
