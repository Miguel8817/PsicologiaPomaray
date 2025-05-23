from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'psicologia'

mysql = MySQL(app)

# RUTAS GENERALES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('iniciar_sesion'))



@app.route('/record', methods=['GET', 'POST'])
def registro_form():
    if request.method == 'POST':
        name = request.form['name']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']

        if not name or not lastName or not email or not password:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('registro.html')

        cur = mysql.connection.cursor()
        try:
            cur.execute('SELECT * FROM user WHERE email = %s', (email,))
            existing_user = cur.fetchone()
            if existing_user:
                flash('El correo electrónico ya está registrado. Por favor, inicie sesión.', 'error')
                return redirect(url_for('registross'))

            hashed_password = generate_password_hash(password)
            cur.execute('INSERT INTO user (name, lastName, email, password) VALUES (%s, %s, %s, %s)',
                        (name, lastName, email, hashed_password))
            mysql.connection.commit()
            session['email'] = email
            flash('Usuario registrado correctamente.', 'success')
            return redirect(url_for('inicio'))

        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'error')
            mysql.connection.rollback()
        finally:
            cur.close()

    return redirect(url_for('registross'))

@app.route('/login', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        ADMIN_CREDENTIALS = {
            'email': "admin@admin.com",
            'password': "12345678"
        }
        if email == ADMIN_CREDENTIALS['email'] and password == ADMIN_CREDENTIALS['password']:
            session['logged_in'] = True
            session['is_admin'] = True
            session['email'] = email
            flash('Bienvenido Administrador!', 'success')
            return redirect(url_for('admin'))

        if not email or not password:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('login.html')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cur.execute('SELECT * FROM user WHERE email = %s', (email,))
            user = cur.fetchone()

            if not user:
                flash('El correo electrónico no está registrado.', 'error')
                return render_template('login.html')

            if check_password_hash(user['password'], password):
                session['email'] = user['email']
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('inicio'))
            else:
                flash('Contraseña incorrecta', 'error')
                return render_template('login.html')

        except Exception as e:
            flash(f'Error al iniciar sesión: {e}', 'error')
            return render_template('login.html')
        finally:
            cur.close()

    return render_template('login.html')

# ADMINISTRACIÓN
@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, lastName, email FROM user")
    users = cur.fetchall()
    cur.close()
    return render_template('admin.html', users=users)

# USUARIOS Y CRUD
@app.route('/usuarios')
def usuario():
    if 'email' not in session:
        flash('Debes iniciar sesión para acceder', 'error')
        return redirect(url_for('iniciar_sesion'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    cursor.close()
    return render_template('usuario.html', user=users)

@app.route('/CRUD')
def CRUD():
    if 'email' not in session:
        flash('Debes iniciar sesión para acceder', 'error')
        return redirect(url_for('logout'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    data = cur.fetchall()
    cur.close()
    return render_template('CRUD.html', users=data)

@app.route('/GUARDAR', methods=['POST'])
def guardar():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    hashed_password = generate_password_hash(password)
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO user (email, name, password) VALUES (%s, %s, %s)", (email, name, hashed_password))
        mysql.connection.commit()
        flash('Usuario agregado correctamente', 'success')
    except Exception as e:
        flash(f'Error al agregar usuario: {e}', 'error')
        mysql.connection.rollback()
    finally:
        cur.close()
    return redirect(url_for('CRUD'))

@app.route('/delete/<string:id>', methods=['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute('DELETE FROM user WHERE id = %s', (id,))
        mysql.connection.commit()
        flash('Usuario eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar usuario: {e}', 'error')
        mysql.connection.rollback()
    finally:
        cur.close()
    return redirect(url_for('CRUD'))

@app.route('/editar/<string:id>', methods=['POST'])
def editar(id):
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password)
    cur = mysql.connection.cursor()
    try:
        cur.execute('UPDATE user SET name = %s, email = %s, password = %s WHERE id = %s', (name, email, hashed_password, id))
        mysql.connection.commit()
        flash('Usuario actualizado correctamente', 'success')
        # Instead of returning jsonify, redirect:
        return redirect(url_for('CRUD'))
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al actualizar el usuario: {str(e)}', 'error')
        return redirect(url_for('CRUD')) # Redirect even on error to show message
    finally:
        cur.close()

# CITAS PSICÓLOGO
@app.route('/GestionCita')
def gestion_citas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cita_psicologo")
    psicologo = cur.fetchall()
    cur.close()
    return render_template('GestionCitas.html', psicologo=psicologo)

@app.route('/guardar_cita', methods=['POST'])
def guardar_cita():
    FechaPS = request.form['FechaPS']
    HoraPS = request.form['HoraPS']
    try:
        datetime.strptime(FechaPS, '%Y-%m-%d')
        datetime.strptime(HoraPS, '%H:%M')
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO cita_psicologo (FechaPS, HoraPS) VALUES (%s, %s)", (FechaPS, HoraPS))
        mysql.connection.commit()
        cursor.close()
        flash('Cita guardada correctamente.', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al guardar la cita: {e}', 'error')
    return redirect(url_for('gestion_citas'))

@app.route('/delete_cita/<int:id>', methods=['POST'])
def delete_cita(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM cita_psicologo WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Cita eliminada correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar la cita: {e}', 'error')
        mysql.connection.rollback()
    finally:
        cursor.close()
    return redirect(url_for('gestion_citas'))

@app.route('/editar_cita/<int:id>', methods=['POST'])
def editar_cita(id):
    fecha = request.form['FechaPS']
    hora = request.form['HoraPS']
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE cita_psicologo SET FechaPS = %s, HoraPS = %s WHERE id = %s", (fecha, hora, id))
        mysql.connection.commit()
        cursor.close()
        flash('Cita editada correctamente', 'success')
        return redirect(url_for('gestion_citas'))
    except Exception as e:
        flash(f'Error al editar la cita: {e}', 'error')
        mysql.connection.rollback()
        return redirect(url_for('gestion_citas'))


# CITAS PROFESOR
@app.route('/Psicologo_cita', methods=['GET', 'POST'])
def agendar_psicologo():
    if 'email' not in session:
        flash('Debes iniciar sesión para agendar una cita.', 'error')
        return redirect(url_for('iniciar_sesion'))

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT id FROM user WHERE email = %s", (session['email'],))
    usuario = cur.fetchone()
    id = usuario['id']
    cur.close()

    if request.method == 'POST':
        FechaPS = request.form['FechaPS']
        HoraPS = request.form['HoraPS']
        print(f"FechaPS: {FechaPS}")
        print(f"HoraPS: {HoraPS}")
        print(f"ID de usuario: {id}")
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO cita_psicologo (FechaPS, HoraPS, id) VALUES (%s, %s, %s)',
                        (FechaPS, HoraPS, id))
            mysql.connection.commit()
            flash('Cita con el psicólogo agendada correctamente', 'success')
        except Exception as e:
            flash(f'Error al agendar cita con el psicólogo: {e}', 'error')
            mysql.connection.rollback()
        finally:
            cur.close()
        return redirect(url_for('agendar_psicologo'))

    # Mostrar solo las citas del usuario actual
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cita_psicologo WHERE id = %s', (id,))
    citas = cur.fetchall()
    cur.close()
    return render_template('agendar_Psicologo.html', citas=citas)


@app.route('/Profesor_cita', methods=['GET', 'POST'])
def agendar_profesor():
    if 'email' not in session:
        flash('Debes iniciar sesión para agendar una cita.', 'error')
        return redirect(url_for('iniciar_sesion'))

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT id FROM user WHERE email = %s", (session['email'],))
    usuario = cur.fetchone()
    id = usuario['id']
    cur.close()

    if request.method == 'POST':
        FechaPR = request.form['FechaPR']
        HoraPR = request.form['HoraPR']
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO cita_profesor (FechaPR, HoraPR) VALUES (%s, %s)', (FechaPR, HoraPR))
            mysql.connection.commit()
            flash('Cita con el profesor agendada correctamente', 'success')
            return redirect(url_for('agendar_profesor')) # Redirigir para mostrar mensaje
        except Exception as e:
            flash(f'Error al agendar cita con el profesor: {e}', 'error')
            mysql.connection.rollback()
            # Podrías optar por renderizar el formulario nuevamente con el error
            return render_template('agendar_Profesor.html')
        finally:
            cur.close()
    else: # request.method == 'GET'
        return render_template('agendar_Profesor.html')
    

@app.route('/GestionProfesor')
def gestion_citas_profesor():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cita_profesor")
    profesor = cur.fetchall()
    cur.close()
    return render_template('GestionProfesor.html', profesor=profesor)

@app.route('/Guardar_cita_profesor', methods=['POST'])
def guardar_cita_profesor():
    FechaPR = request.form['FechaPR']
    HoraPR = request.form['HoraPR']
    try:
        datetime.strptime(FechaPR, '%Y-%m-%d')
        datetime.strptime(HoraPR, '%H:%M')
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO cita_profesor (FechaPR, HoraPR) VALUES (%s, %s)", (FechaPR, HoraPR))
        mysql.connection.commit()
        cursor.close()
        flash('Cita guardada correctamente.', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al guardar la cita: {e}', 'error')
    return redirect(url_for('gestion_citas_profesor'))

@app.route('/Delete_cita_profesor/<int:id>', methods=['POST'])
def delete_cita_profesor(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM cita_profesor WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Cita eliminada correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar la cita: {e}', 'error')
        mysql.connection.rollback()
    finally:
        cursor.close()
    return redirect(url_for('gestion_citas_profesor'))

@app.route('/Editar_cita_profesor/<int:id>', methods=['POST'])
def editar_cita_profesor(id):
    FechaPR = request.form['FechaPR']
    HoraPR = request.form['HoraPR']
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE cita_profesor SET FechaPR = %s, HoraPR = %s WHERE id = %s", (FechaPR, HoraPR, id))
        mysql.connection.commit()
        cursor.close()
        flash('Cita editada correctamente', 'success')
        return redirect(url_for('gestion_citas_profesor'))
    except Exception as e:
        flash(f'Error al editar la cita: {e}', 'error')
        mysql.connection.rollback()
        return redirect(url_for('gestion_citas_profesor'))

if __name__ == '__main__':
    app.run(debug=True)