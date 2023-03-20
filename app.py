from flask import Flask, render_template, request, url_for, redirect
import database as db
app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('mostrarComentarios'))

@app.route("/index.html")
def home():
    return redirect(url_for('mostrarComentarios'))

@app.route("/mostrarComments")
def mostrarComentarios():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM comments")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

@app.route('/addComment', methods=['POST'])
def addComments():
     # Recupera los datos ingresados por el usuario en el input
    fullname = request.form['full_name']
    email = request.form['email']
    comment = request.form['comment']

    # Insertar el comentario en la base de datos
    cursor = db.database.cursor()
    # Insertar usuario nuevo dentro de la tabla users
    sql = "INSERT INTO comments (fullname, email, comment) VALUES (%s, %s, %s);"
    values = (fullname, email, comment)

    # Ejecutar la consulta SQL y obtener los resultados
    cursor.execute(sql, values)

    if cursor.rowcount > 0:
        db.database.commit()
        #reg_success_msg = "Se registro el comentario exitosamente!"
        return redirect(url_for('mostrarComentarios'))
    else:
        # Error al registrar usuario, mostrar mensaje de error al usuario
        #reg_error_msg = "No se pudo registrar el comentario"
        #return render_template('index.html', reg_error_msg=reg_error_msg)
        print("No se pudo registar el comentario")
        return redirect(url_for('mostrarComentarios'))

if __name__ == "__main__":
    app.run(debug = True, port=4000, host="0.0.0.0")