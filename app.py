from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify, abort
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["ENV"] = os.getenv("FLASK_ENV", "production")  
app.config["DEBUG"] = app.config["ENV"] == "development"

# Configuración MySQL
app.config['MYSQL_HOST'] = 'gondola.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'BvStTwybTRaXZGUreUdqUPZKEwVWatPK'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = '14068'
mysql = MySQL(app)

# -------------------- RUTAS GENERALES --------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('iniciar_sesion'))

@app.route('/record', methods=['GET', 'POST'])
def record():
    if request.method == 'POST':
        name = request.form['name']
        lastName = request.form['lastName']
        email = request.form['email'].lower().strip()
        password = request.form['password']

        if not all([name, lastName, email, password]):
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('registro.html')

        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'error')
            return render_template('registro.html')

        cur = mysql.connection.cursor()
        try:
            cur.execute('SELECT * FROM user WHERE email = %s', (email,))
            if cur.fetchone():
                flash('El correo ya está registrado.', 'error')
                return redirect(url_for('iniciar_sesion'))

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            
            cur.execute(
                'INSERT INTO user (name, lastName, email, password) VALUES (%s, %s, %s, %s)',
                (name, lastName, email, hashed_password)
            )
            mysql.connection.commit()
            
            session['email'] = email
            flash('Registro exitoso.', 'success')
            return redirect(url_for('usuario'))
        except Exception as e:
            mysql.connection.rollback()
            app.logger.error(f'Error al registrar usuario: {str(e)}')
            flash('Error técnico al registrar. Por favor intente nuevamente.', 'error')
        finally:
            cur.close()
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('login.html')

        # Verificación de administrador
        if email == "admin@admin.com":
            if password == "12345678":
                session.update({
                    'logged_in': True,
                    'is_admin': True,
                    'email': email,
                    'user_id': 0
                })
                flash('Bienvenido Administrador!', 'success')
                return redirect(url_for('admin'))
            flash('Credenciales incorrectas', 'error')
            return render_template('login.html')

        cursor = None
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT id, name, email, password FROM user WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                flash('Credenciales incorrectas', 'error')
                return render_template('login.html')
            
            if not check_password_hash(user['password'], password):
                flash('Credenciales incorrectas', 'error')
                return render_template('login.html')
            
            session.update({
                'logged_in': True,
                'user_id': user['id'],
                'email': user['email'],
                'name': user.get('name', '')
            })
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('usuario'))
            
        except Exception as e:
            app.logger.error(f"Error inesperado: {str(e)}")
            flash('Error técnico al iniciar sesión', 'error')
        finally:
            if cursor:
                cursor.close()
    
    return render_template('login.html')

# -------------------- ADMINISTRADOR --------------------

@app.route('/admin')
def admin():
    # Verificación mejorada de administrador
    if not session.get('is_admin') or not session.get('logged_in'):
        flash('Debes iniciar sesión como administrador para acceder a esta página', 'error')
        return redirect(url_for('iniciar_sesion'))
    
    
        # Resto del código...
    
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM user) AS total_usuarios,
                    (SELECT COUNT(*) FROM cita_psicologo) AS citas_psicologo,
                    (SELECT COUNT(*) FROM cita_profesor) AS citas_profesor,
                    (SELECT COUNT(*) FROM user WHERE created_at >= CURDATE() - INTERVAL 7 DAY) AS nuevos_usuarios,
                    (SELECT COUNT(*) FROM cita_psicologo WHERE FechaPS >= CURDATE()) AS citas_hoy_psi,
                    (SELECT COUNT(*) FROM cita_profesor WHERE FechaPR >= CURDATE()) AS citas_hoy_prof
            """)
            stats = cursor.fetchone()
            
            cursor.execute("""
                SELECT id, name, lastName, email, created_at 
                FROM user 
                ORDER BY created_at DESC 
                LIMIT 10
            """)
            users = cursor.fetchall()
            
        return render_template('admin.html', users=users, stats=stats)
        
    except Exception as e:
        app.logger.error(f"Error en panel admin: {str(e)}")
        flash('Error al cargar el panel de administración', 'error')
        return redirect(url_for('index'))

# -------------------- USUARIOS CRUD --------------------

@app.route('/usuarios')
def usuario():
    if 'email' not in session:
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('iniciar_sesion'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    cursor.close()
    return render_template('usuario.html', user=users)

@app.route('/CRUD')
def CRUD():
    if 'email' not in session:
        return redirect(url_for('logout'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    users = cur.fetchall()
    cur.close()
    return render_template('CRUD.html', users=users)

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
        flash('Usuario agregado', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {e}', 'error')
    finally:
        cur.close()
    return redirect(url_for('CRUD'))

@app.route('/delete/<string:id>', methods=['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute('DELETE FROM user WHERE id = %s', (id,))
        mysql.connection.commit()
        flash('Usuario eliminado', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {e}', 'error')
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
        cur.execute('UPDATE user SET name = %s, email = %s, password = %s WHERE id = %s', 
                   (name, email, hashed_password, id))
        mysql.connection.commit()
        flash('Usuario actualizado', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {e}', 'error')
    finally:
        cur.close()
    return redirect(url_for('CRUD'))

# -------------------- CITAS PSICÓLOGO --------------------

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
        flash('Cita guardada', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {e}', 'error')
    return redirect(url_for('gestion_citas'))

@app.route('/delete_cita/<int:id>', methods=['POST'])
def delete_cita(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM cita_psicologo WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Cita eliminada', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {e}', 'error')
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
        flash('Cita editada', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {e}', 'error')
    return redirect(url_for('gestion_citas'))

@app.route('/Psicologo_cita', methods=['GET', 'POST'])
def agendar_psicologo():
    if 'email' not in session:
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('iniciar_sesion'))

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT id FROM user WHERE email = %s", (session['email'],))
    user = cur.fetchone()
    user_id = user['id']
    cur.close()

    if request.method == 'POST':
        FechaPS = request.form['FechaPS']
        HoraPS = request.form['HoraPS']
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO cita_psicologo (FechaPS, HoraPS, id) VALUES (%s, %s, %s)", 
                       (FechaPS, HoraPS, user_id))
            mysql.connection.commit()
            flash('Cita agendada', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error: {e}', 'error')
        finally:
            cur.close()
        return redirect(url_for('agendar_psicologo'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cita_psicologo WHERE id = %s", (user_id,))
    citas = cur.fetchall()
    cur.close()
    return render_template('agendar_Psicologo.html', citas=citas)

# -------------------- CITAS PROFESOR --------------------

@app.route('/Profesor_cita', methods=['GET', 'POST'])
def agendar_profesor():
    if 'email' not in session:
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('iniciar_sesion'))

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT id FROM user WHERE email = %s", (session['email'],))
    user = cur.fetchone()
    user_id = user['id']
    cur.close()

    if request.method == 'POST':
        FechaPR = request.form['FechaPR']
        HoraPR = request.form['HoraPR']
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO cita_profesor (FechaPR, HoraPR, id) VALUES (%s, %s, %s)", 
                       (FechaPR, HoraPR, user_id))
            mysql.connection.commit()
            flash('Cita agendada', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error: {e}', 'error')
        finally:
            cur.close()
        return redirect(url_for('agendar_profesor'))

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
        flash('Cita guardada', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {e}', 'error')
    return redirect(url_for('gestion_citas_profesor'))

@app.route('/Delete_cita_profesor/<int:id>', methods=['POST'])
def delete_cita_profesor(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM cita_profesor WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Cita eliminada', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {e}', 'error')
    finally:
        cursor.close()
    return redirect(url_for('gestion_citas_profesor'))

@app.route('/Editar_cita_profesor/<int:id>', methods=['POST'])
def editar_cita_profesor(id):
    FechaPR = request.form['FechaPR']
    HoraPR = request.form['HoraPR']
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE cita_profesor SET FechaPR = %s, HoraPR = %s WHERE id = %s", 
                       (FechaPR, HoraPR, id))
        mysql.connection.commit()
        flash('Cita editada', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {e}', 'error')
    return redirect(url_for('gestion_citas_profesor'))

# -------------------- INICIAR APLICACIÓN --------------------

if __name__ == '__main__':
    app.run(debug=True)