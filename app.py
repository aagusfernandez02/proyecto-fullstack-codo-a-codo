from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'codo-a-codo'
mysql = MySQL(app)

@app.route("/")
def index():
    return redirect("/movies/get")

@app.route("/movies/get")
def getMovies():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM peliculas")
    peliculas = cursor.fetchall()
    cursor.close()
    return render_template("/peliculas/peliculas.html", peliculas=peliculas)

@app.route("/movies/create")
def createMovieForm():
    return render_template("/peliculas/createMovie.html")

@app.route("/movies/create", methods=['POST'])
def createMovie():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    duracion = request.form['duracion']
    img = request.form['img']
    director = request.form['director']
    anio_estreno = request.form['anio_estreno']

    query = f"INSERT INTO `peliculas`(`nombre`, `descripcion`, `duracion`, `img`, `director`, `anio_estreno`) VALUES ('{nombre}', '{descripcion}', '{duracion}', '{img}', '{director}', '{anio_estreno}')"
    print(query)
    conn = mysql.connection 
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

    return redirect('/movies/get')
    
@app.route("/movies/edit")
def editMovieForm():
    id = request.args.get('id')
    query = f"SELECT * FROM `peliculas` WHERE id = {id}"

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(query)
    pelicula = cursor.fetchall()
    
    cursor.close()
    return render_template("/peliculas/editMovie.html", pelicula=pelicula)

@app.route("/movies/edit", methods=['POST'])
def editMovie():
    id = request.form['id']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    duracion = request.form['duracion']
    img = request.form['img']
    director = request.form['director']
    anio_estreno = request.form['anio_estreno']

    query = f"UPDATE `peliculas` SET `nombre` = '{nombre}', `duracion` = '{duracion}', `descripcion` = '{descripcion}', `img` = '{img}', `director` = '{director}', `anio_estreno` = '{anio_estreno}' WHERE `peliculas`.`id` = {id}"

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

    return redirect('/movies/get')

@app.route("/movies/delete")
def deleteMovie():
    id = request.args.get('id')
    query = f"DELETE FROM `peliculas` WHERE `peliculas`.`id` = {id}"

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    cursor.close()
    return redirect('/movies/get')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)