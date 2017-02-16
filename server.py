from flask import Flask, render_template,request,jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/enternew')
def enternew():
    return render_template('food.html')

@app.route('/addfood', methods = ['POST'])
def addfood():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        name = request.form['name']
        calories = request.form['calories']
        cuisine = request.form['cuisine']
        is_vegetarian = request.form['is_vegetarian']
        is_gluten_free = request.form['is_gluten_free']
        cursor.execute('INSERT INTO foods (name,calories,cuisine,is_vegetarian,is_gluten_free) VALUES (?,?,?,?,?)', (name,calories,cuisine,is_vegetarian,is_gluten_free))
        connection.commit()
        message = 'Record successfully added'
    except:
        connection.rollback()
        message = 'error in insert operation'
    finally:
        connection.close()
        return render_template('result.html', message = message)

@app.route('/favorite')
def favorite():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM foods WHERE name = "Dust Cakes"')
    except:
        result = ["DATABASE ERROR"]
    finally:
        result = cursor.fetchone()
        connection.close()

    return jsonify(result)

@app.route('/search')
def search():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    name = (request.args.get('name'),)
    try:
        cursor.execute('SELECT * FROM foods where name = ?', name)
        result = jsonify(results=cursor.fetchall())
    except:
        result = "Database Error"
    finally:
        connection.close()

    return result

@app.route('/drop')
def drop():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute('DROP TABLE foods')
        result = 'dropped'
    except:
        result = 'error'
    finally:
        connection.close()
        return result
