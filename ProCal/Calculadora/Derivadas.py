from flask import Blueprint, render_template, request
import sympy as sp
import re

Derivadas = Blueprint('Derivadas', __name__)

def limpiar_entrada(entrada):
    entrada = entrada.replace('^', '**').replace('ˆ', '**')  # Reemplaza ^ o ˆ por **
    entrada = entrada.replace('X', 'x').replace(' ', '')     # Convierte X mayúscula a x y elimina espacios
    # Inserta el operador * donde falte, por ejemplo en 2x → 2*x
    entrada = re.sub(r'(\d)(x)', r'\1*\2', entrada)
    return entrada

@Derivadas.route('/derivadas', methods=['GET', 'POST'])
def derivadas():
    resultados = []
    error = None

    if request.method == 'POST':
        metodo = request.form['metodo']  # 'rolle', 'valor_medio', 'max_min'
        funcion_str = request.form['funcion']
        a = request.form.get('a', '')
        b = request.form.get('b', '')

        # Validar inputs numéricos solo si existen
        try:
            a = float(a) if a else None
            b = float(b) if b else None
        except ValueError:
            error = "Los valores de 'a' y 'b' deben ser numéricos."
            return render_template('Derivadas.html', resultados=[], error=error)

        # Procesar función
        expr_text = limpiar_entrada(funcion_str).lower()

        # Definir símbolo x
        x = sp.symbols('x')

        try:
            funcion = sp.sympify(expr_text)
            derivada = sp.diff(funcion, x)
            segunda_derivada = sp.diff(derivada, x)
        except (sp.SympifyError, SyntaxError) as err:
            error = f"Función inválida: {err}"
            return render_template('Derivadas.html', resultados=[], error=error)

        # Resolver según método
        if metodo == 'rolle':
            if a is None or b is None:
                error = "Debe ingresar los valores de a y b para el Teorema de Rolle."
            else:
                resultados = teorema_rolle(funcion, derivada, x, a, b)

        elif metodo == 'valor_medio':
            if a is None or b is None:
                error = "Debe ingresar los valores de a y b para el Teorema del Valor Medio."
            else:
                resultados = teorema_valor_medio(funcion, derivada, x, a, b)

        elif metodo == 'max_min':
            resultados = maximos_minimos(funcion, derivada, segunda_derivada, x)

        else:
            error = "Método no válido seleccionado."

    return render_template('Derivadas.html', resultados=resultados, error=error)

# Implementación Teorema de Rolle
def teorema_rolle(f, f_prime, x, a, b):
    resultados = []
    # Condiciones para Rolle:
    # 1) f continua en [a,b] (asumimos sí)
    # 2) f derivable en (a,b) (asumimos sí)
    # 3) f(a) == f(b)
    if f.subs(x, a) != f.subs(x, b):
        resultados.append({'error': 'No se cumple f(a) = f(b). Teorema de Rolle no aplica.'})
        return resultados

    # Buscar puntos c en (a,b) donde f'(c) = 0
    criticos = sp.solveset(f_prime, x, domain=sp.Interval(a, b))

    # Filtrar soluciones reales dentro (a,b)
    criticos_reales = [c.evalf() for c in criticos if c.is_real and a < c.evalf() < b]

    if not criticos_reales:
        resultados.append({'info': 'No se encontraron puntos c en (a,b) donde f\'(c) = 0.'})
    else:
        for c in criticos_reales:
            resultados.append({'c': float(c), 'f_prime_c': float(f_prime.subs(x, c))})

    return resultados

# Implementación Teorema del Valor Medio
def teorema_valor_medio(f, f_prime, x, a, b):
    resultados = []
    # Pendiente media
    m = (f.subs(x, b) - f.subs(x, a)) / (b - a)
    resultados.append({'pendiente_media': float(m)})

    # Buscar c en (a,b) tal que f'(c) = m
    eq = sp.Eq(f_prime, m)
    soluciones = sp.solveset(eq, x, domain=sp.Interval(a, b))

    soluciones_reales = [c.evalf() for c in soluciones if c.is_real and a < c.evalf() < b]

    if not soluciones_reales:
        resultados.append({'info': 'No se encontraron puntos c en (a,b) que satisfagan f\'(c) = pendiente media.'})
    else:
        for c in soluciones_reales:
            resultados.append({'c': float(c), 'f_prime_c': float(f_prime.subs(x, c))})

    return resultados

# Implementación Máximos y Mínimos
def maximos_minimos(f, f_prime, f_2prime, x):
    resultados = []
    # Encontrar puntos críticos f'(x)=0
    criticos = sp.solveset(f_prime, x, domain=sp.S.Reals)

    # Evaluar segunda derivada para determinar tipo de punto
    for c in criticos:
        if c.is_real:
            valor_2da = f_2prime.subs(x, c)
            if valor_2da > 0:
                tipo = 'Mínimo local'
            elif valor_2da < 0:
                tipo = 'Máximo local'
            else:
                tipo = 'Punto de inflexión o indeterminado'
            resultados.append({
                'punto': float(c.evalf()),
                'tipo': tipo,
                'f(punto)': float(f.subs(x, c).evalf())
            })

    if not resultados:
        resultados.append({'info': 'No se encontraron puntos críticos reales.'})

    return resultados
