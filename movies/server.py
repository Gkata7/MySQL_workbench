from flask import Flask, render_template, redirect, session,request
from mysqlconnection import MySQLConnection

app = Flask(__name__)
app.secret_key = 'movies'
mysql = MySQLConnection(app,'moviedb')

@app.route('/')
def index():
    query = 'SELECT id, title, stars, release_date FROM movies'
    session['movies'] = mysql.query_db(query)
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/add_movie', methods=['POST'])
def add_movie():
    query = '''INSERT INTO movies (title,stars,release_date,img_src,description,created_at)
                VALUES (:title, :stars, :release_date, :img_src, :description, NOW())'''
    data = {
        'title':request.form['title'],
        'stars':request.form['stars'],
        'release_date':request.form['release_date'],
        'img_src':request.form['img_src'],
        'description':request.form['desc']
    }
    mysql.query_db(query,data)
    return redirect('/')

@app.route('/show/<id>')
def show(id):
    query = 'SELECT title,stars,release_date,img_src,description FROM movies where id = :id'
    data = {
        'id' : id
    }
    result = mysql.query_db(query,data)[0]
    return render_template('show.html',path=result['img_src'],title=result['title'],stars=result['stars'],release_date=result['release_date'],
                            description=result['description'])

@app.route('/edit/<id>',methods=['GET'])
def edit(id):
    query = 'SELECT title,stars,release_date,img_src,description FROM movies where id = :id'
    data = {
        'id' : id
    }
    result = mysql.query_db(query,data)[0]
    return render_template('update.html',id=id,path=result['img_src'],title=result['title'],stars=result['stars'],release_date=result['release_date'],
                        img_src=result['img_src'],description=result['description'])

@app.route('/update/<id>',methods=['POST'])
def update(id):
    query = 'UPDATE movies SET title=:title, stars=:stars, release_date=:release_date,img_src=:img_src,description=:description, updated_at=now() where id = :id'
    data = {
        'title':request.form['title'],
        'stars':request.form['stars'],
        'release_date':request.form['release_date'],
        'img_src':request.form['img_src'],
        'description':request.form['desc'],
        'id' : id
    }
    mysql.query_db(query,data)
    return redirect('/')

@app.route('/delete/<id>',methods=['GET'])
def render_delete(id):
    return render_template('delete.html',id=id)

@app.route('/delete_user/<id>',methods=['POST'])
def delete(id):
    if request.form['delete_action'] == 'yes':
        query = 'DELETE FROM movies WHERE id = :id'
        data = {
            'id':id
        }
        mysql.query_db(query,data)
    return redirect('/')
app.run(debug=True)
