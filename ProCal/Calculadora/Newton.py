from flask import Blueprint, render_template, request
import sympy as sp
import re

Newton = Blueprint('Newton', __name__)

@Newton.route('/newton', methods=['GET', 'POST'])
def newton():
    resultados = []

    if request.method == 'POST':
        # 1) Leer datos
        funcion_str = request.form['funcion']
        x0          = float(request.form['x0'])
        tolerancia  = abs(float(request.form['tolerancia']))

        # 2) Definir símbolo
        x = sp.symbols('x')

        # 3) Reemplazar ^→**, forzar minúsculas
        expr_text = funcion_str.replace('^', '**').lower()

        # 4) Insertar '*' implícitos (6x → 6*x, x2 → x*2)
        expr_text = re.sub(r'(?<=\d)(?=[a-z])', '*', expr_text)
        expr_text = re.sub(r'(?<=[a-z])(?=\d)', '*', expr_text)

        # 5) Sympify + derivar
        try:
            funcion  = sp.sympify(expr_text)
            derivada = sp.diff(funcion, x)
        except (sp.SympifyError, SyntaxError) as err:
            resultados = [{'error': f"Función inválida: {err}"}]
            return render_template('Newton.html', resultados=resultados)

        # 6) Lambdify
        f     = sp.lambdify(x, funcion,  'math')
        f_der = sp.lambdify(x, derivada, 'math')

        # 7) Newton–Raphson
        xi = x0
        max_iter = 100
        for i in range(1, max_iter + 1):
            fx  = f(xi)
            fdx = f_der(xi)
            if fdx == 0:
                resultados = [{'error': "Derivada cero. No se puede continuar."}]
                break

            xr = xi - fx / fdx

            # error = 0 en la primera iteración, luego el real
            if i == 1:
                err_abs = 0.0
            else:
                err_abs = abs(xr - xi)

            resultados.append({
                'iteracion':  i,
                'x':           round(xi,     4),
                'fx':          round(fx,     4),
                'fdx':         round(fdx,    4),
                'x1':          round(xr,     4),
                'error_abs':   round(err_abs,4)
            })

            # Solo romper si YA pasamos la primera iteración y cumplimos tolerancia
            if i > 1 and err_abs < tolerancia:
                break

            xi = xr

    return render_template('Newton.html', resultados=resultados)
