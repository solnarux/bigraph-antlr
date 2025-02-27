from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from bigraph_symbol_table import BigraphSymbolTable

class SemanticAnalyzer(SimpleLangVisitor):
    def __init__(self):
        super().__init__()
        self.symbol_table = BigraphSymbolTable()
        self.current_scope = "global"

        # Agregar ámbito global al bigrafo
        self.symbol_table.add_scope(self.current_scope)

    def visitVarDecl(self, ctx: SimpleLangParser.VarDeclContext):
        """Procesa declaraciones de variables."""
        var_name = ctx.ID().getText()
        self.symbol_table.add_symbol(var_name, self.current_scope)
        return self.visitChildren(ctx)

    def visitAssignStmt(self, ctx: SimpleLangParser.AssignStmtContext):
        """Procesa asignaciones, registrando dependencias."""
        var_name = ctx.ID().getText()
        expr_symbols = [t.getText() for t in ctx.expr().getTokens(SimpleLangParser.ID)]
        
        # Registrar variable si no está en la tabla
        if var_name not in self.symbol_table.symbol_table:
            self.symbol_table.add_symbol(var_name, self.current_scope)

        # Registrar dependencia en el hipergrafo
        self.symbol_table.add_dependency([var_name] + expr_symbols)
        return self.visitChildren(ctx)

    def analyze(self, tree):
        """Ejecuta el análisis semántico recorriendo el árbol."""
        self.visit(tree)
        self.symbol_table.show_forest()
        self.symbol_table.show_hypergraph()
