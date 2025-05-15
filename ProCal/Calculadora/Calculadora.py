from flask import Blueprint, render_template, request, jsonify
from asteval import Interpreter
import math

Calculadora = Blueprint('Calculadora', __name__)

@Calculadora.route('/Calculadora', methods=['GET','POST'])
def mostrar_calculadora():
    return render_template('Calculadora.html')

@Calculadora.route('/api/calcular', methods=['POST'])
def calcular():
    data = request.get_json()
    expresion = data.get('expresion', '')
    modo = data.get('modo', 'DEG')

    aeval = Interpreter()

    # Definir funciones personalizadas con modo DEG/RAD
    def deg(x): return math.radians(x)
    def rad(x): return math.degrees(x)
    def fact(x):
        if not (isinstance(x, (int, float)) and x >= 0 and x == int(x)):
            raise ValueError("Factorial solo para enteros no negativos")
        return math.factorial(int(x))

    # Añadir funciones y constantes a asteval
    aeval.symtable.update({
        'sin': lambda x: math.sin(deg(x)) if modo == 'DEG' else math.sin(x),
        'cos': lambda x: math.cos(deg(x)) if modo == 'DEG' else math.cos(x),
        'tan': lambda x: math.tan(deg(x)) if modo == 'DEG' else math.tan(x),
        'asin': lambda x: rad(math.asin(x)) if modo == 'DEG' else math.asin(x),
        'acos': lambda x: rad(math.acos(x)) if modo == 'DEG' else math.acos(x),
        'atan': lambda x: rad(math.atan(x)) if modo == 'DEG' else math.atan(x),
        'log': math.log10,
        'ln': math.log,
        'sqrt': math.sqrt,
        'exp': math.exp,
        'fact': fact,
        'pi': math.pi,
        'e': math.e,
        '^': '**'
    })

    try:
        # Reemplazar ^ por ** para potencia
        expresion = expresion.replace('^', '**')
        resultado = aeval(expresion)

        # Verificar errores del intérprete
        if aeval.error:
            raise ValueError(aeval.error[0].get_error())

        return jsonify({'resultado': resultado})
    except Exception as e:
        return jsonify({'resultado': f'Error: {str(e)}'})
