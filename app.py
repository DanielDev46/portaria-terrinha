from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "minha_chave_secreta"

# Página de login/cadastro
@app.route("/")
def index():
    return render_template("index.html")

# Login
@app.route("/login", methods=["POST"])
def login():
    nome = request.form.get("usuario")
    senha = request.form.get("senha")

    with open("usuarios.json", "r") as f:
        usuarios = json.load(f)

    if nome in usuarios and usuarios[nome] == senha:
        session["usuario"] = nome
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html", erro="Usuário ou senha inválidos.")

# Cadastro de novo usuário
@app.route("/cadastro", methods=["POST"])
def cadastro():
    nome = request.form.get("usuario")
    senha = request.form.get("senha")

    with open("usuarios.json", "r") as f:
        usuarios = json.load(f)

    if nome in usuarios:
        return render_template("index.html", erro="Usuário já existe.")
    
    usuarios[nome] = senha
    with open("usuarios.json", "w") as f:
        json.dump(usuarios, f)
    
    return redirect(url_for("index"))

# Página principal após login
@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html", usuario=session["usuario"])

# Cadastrar nova placa
@app.route("/cadastrar_placa", methods=["POST"])
def cadastrar_placa():
    if "usuario" not in session:
        return redirect(url_for("index"))

    placa = request.form["placa"]
    motorista = request.form["motorista"]
    veiculo = request.form["veiculo"]

    with open("placas.json", "r") as f:
        placas = json.load(f)

    placas[placa] = {
        "placa": placa,
        "motorista": motorista,
        "veiculo": veiculo
    }

    with open("placas.json", "w") as f:
        json.dump(placas, f, indent=4)

    return redirect(url_for("dashboard"))

# Consultar placa
@app.route("/consultar_placa", methods=["POST"])
def consultar_placa():
    if "usuario" not in session:
        return redirect(url_for("index"))

    placa = request.form["placa"]

    with open("placas.json", "r") as f:
        placas = json.load(f)

    resultado = placas.get(placa)
    return render_template("dashboard.html", usuario=session["usuario"], resultado=resultado)

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
