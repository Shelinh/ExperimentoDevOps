from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from database import criar_banco, conectar

app = Flask(__name__)
app.secret_key = "chave_secreta_sistemas_info"

# Garante a criação da tabela e do admin inicial no banco
criar_banco()

@app.route("/")
def index():
    if "usuario" in session:
        if session.get("nivel") == "admin":
            return redirect(url_for("usuarios"))
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["senha"], senha):
            session["usuario"] = user["usuario"]
            session["nivel"] = user["nivel"]
            session["nome"] = user["nome"]

            if user["nivel"] == "admin":
                return redirect(url_for("usuarios"))
            return redirect(url_for("home"))

        flash("Usuário ou senha inválidos.", "danger")

    return render_template("login.html")

@app.route("/home")
def home():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/usuarios")
def usuarios():
    if "usuario" not in session or session.get("nivel") != "admin":
        return redirect(url_for("login"))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios ORDER BY id DESC")
    lista = cursor.fetchall()
    conn.close()

    return render_template("usuarios.html", usuarios=lista)

@app.route("/usuarios/novo", methods=["GET", "POST"])
def novo_usuario():
    if "usuario" not in session or session.get("nivel") != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        nome = request.form["nome"]
        usuario = request.form["usuario"]
        senha = generate_password_hash(request.form["senha"])
        nivel = request.form["nivel"]

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, usuario, senha, nivel) VALUES (?, ?, ?, ?)",
                (nome, usuario, senha, nivel)
            )
            conn.commit()
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("usuarios"))
        except sqlite3.IntegrityError:
            flash("Erro: Este nome de usuário já está em uso.", "danger")
        finally:
            conn.close()

    return render_template("novo_usuario.html")

@app.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    if "usuario" not in session or session.get("nivel") != "admin":
        return redirect(url_for("login"))

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form["nome"]
        usuario = request.form["usuario"]
        nivel = request.form["nivel"]
        nova_senha = request.form["senha"]

        # Se o usuário preencheu a senha, atualiza o hash; caso contrário, mantém a senha atual
        if nova_senha.strip():
            senha_hash = generate_password_hash(nova_senha)
            cursor.execute(
                "UPDATE usuarios SET nome=?, usuario=?, senha=?, nivel=? WHERE id=?",
                (nome, usuario, senha_hash, nivel, id)
            )
        else:
            cursor.execute(
                "UPDATE usuarios SET nome=?, usuario=?, nivel=? WHERE id=?",
                (nome, usuario, nivel, id)
            )

        conn.commit()
        conn.close()
        flash("Dados do usuário atualizados com sucesso!", "success")
        return redirect(url_for("usuarios"))

    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()

    return render_template("editar_usuario.html", usuario=user)

@app.route("/usuarios/excluir/<int:id>")
def excluir_usuario(id):
    if "usuario" not in session or session.get("nivel") != "admin":
        return redirect(url_for("login"))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash("Usuário removido com sucesso!", "warning")
    return redirect(url_for("usuarios"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)