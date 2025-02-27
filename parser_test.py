from antlr4 import FileStream, CommonTokenStream
from SimpleLangLexer import SimpleLangLexer
from SimpleLangParser import SimpleLangParser

def parse_input(file_path):
    # Leer el archivo de código fuente
    input_stream = FileStream(file_path)
    
    # Crear el lexer y el parser
    lexer = SimpleLangLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = SimpleLangParser(tokens)

    # Construir el árbol sintáctico
    tree = parser.program()
    print(tree.toStringTree(recog=parser))  # Imprimir el árbol en consola

# Ejecutar con un archivo de prueba
if __name__ == "__main__":
    parse_input("test.lang")  # Debes crear este archivo con código de prueba
