from flask import Flask, redirect, url_for
from Calculadora.Calculadora import Calculadora
from Calculadora.Grafica import Graficador
from Calculadora.Newton import Newton
from Calculadora.Derivadas import Derivadas

app = Flask(__name__)

# Registramos los Blueprints
app.register_blueprint(Calculadora)
app.register_blueprint(Graficador)
app.register_blueprint(Newton)
app.register_blueprint(Derivadas)

# Ruta principal: redirige a Calculadora
@app.route('/')
def index():
    return redirect(url_for('Calculadora.mostrar_calculadora'))

if __name__ == '__main__':
    app.run(debug=True)
