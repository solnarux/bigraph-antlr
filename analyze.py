from antlr4 import FileStream, CommonTokenStream
from SimpleLangLexer import SimpleLangLexer
from SimpleLangParser import SimpleLangParser
from SemanticAnalyzer import SemanticAnalyzer

def analyze_code(file_path):
    input_stream = FileStream(file_path)
    lexer = SimpleLangLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = SimpleLangParser(tokens)

    tree = parser.program()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(tree)

    

if __name__ == "__main__":
    analyze_code("test.lang")
