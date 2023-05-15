from flask import Flask, render_template, request
import ply.lex as lex

# Definir la lista de tokens y expresiones regulares como en el ejemplo anterior
tokens = (
   'ID',
   'ENTERO',
   'SUMA',
   'RESTA',
   'MULTIPLICACION',
   'DIVISION',
   'ASIGNACION',
   'COMENTARIO',
   'SIMBOLO',
   'PALABRA_RESERVADA',
   'NUMERO',
   'OPERACION',
)

t_SUMA = r'\+'
t_RESTA = r'\-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'\/'
t_ASIGNACION = r'\='
t_COMENTARIO = r'\/\/.*'
t_SIMBOLO = r'[,;:(){}]'
t_OPERACION = r'[\+\-\*\/]'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
reservadas = {
    'int': 'INT',
    'do': 'DO',
    'while': 'WHILE',
    'if': 'IF',
    'for': 'FOR',
    'else': 'ELSE',
}
t_PALABRA_RESERVADA = r'\b(' + '|'.join(reservadas.keys()) + r')\b'


def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore  = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Crear la aplicación Flask
app = Flask(__name__)

# Definir la página de inicio y resultados
@app.route('/', methods=['GET', 'POST'])
def compilador():
    codigo_fuente = ''
    tokens = []
    token_counts = {} # diccionario para mantener un registro del conteo de tokens

    if request.method == 'POST':
        # Obtener el código fuente del formulario
        codigo_fuente = request.form['codigo_fuente']


        # Configurar el lexer con el código fuente
        lexer.input(codigo_fuente)

        # Obtener los tokens
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok)

            # Incrementar el contador de tokens
            if tok.value in token_counts:
                token_counts[tok.value] += 1
            else:
                token_counts[tok.value] = 1

    # Mostrar el formulario y los resultados en la página
    return render_template('index.html', codigo_fuente=codigo_fuente, tokens=tokens, token_counts=token_counts)


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
