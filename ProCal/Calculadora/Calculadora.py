from flask import Blueprint, render_template, request, jsonify
import math
Calculadora = Blueprint('Calculadora', __name__)

@Calculadora.route('/Calculadora')
def mostrar_calculadora():
    return render_template('Calculadora.html')

@Calculadora.route('/Calcular', methods=['GET','POST'])
def calcular():
    data = request.get_json()
    expresion = data.get('expresion', '')
    modo = data.get('modo', 'DEG')

    try:
        def deg(x): return math.radians(x)
        def rad(x): return math.degrees(x)
        def fact(x): return math.factorial(int(x))

        allowed_names = {
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
            '__builtins__': {}
        }
        result = eval(expresion.replace('^', '**'), allowed_names)
        return jsonify({'resultado': result})
    except Exception:
        return jsonify({'resultado': 'Error'})
