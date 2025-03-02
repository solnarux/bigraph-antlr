from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from bigraph_symbol_table import BigraphSymbolTable
from SemanticTreeBuilder import SemanticTreeBuilder
import re

class SemanticAnalyzer(SimpleLangVisitor):
    def __init__(self):
        super().__init__()
        self.symbol_table = BigraphSymbolTable()
        self.current_scope = "global"

        # Agregar ámbito global al bigrafo
        self.symbol_table.add_scope(self.current_scope)

    def visitVarDecl(self, ctx: SimpleLangParser.VarDeclContext):
        """Procesa declaraciones de variables con su tipo."""
        var_name = ctx.ID().getText()
        var_type = ctx.type_().getText()
        var_value = ctx.expr().getText() if ctx.expr() else None
        location = (ctx.start.line, ctx.start.column)
        # Pass additional metadata (AST node and location) to your symbol table
        self.symbol_table.add_symbol(var_name, self.current_scope, "var", var_type, var_value ,ast_node=ctx, location=location)
        
        expr_symbols = ctx.expr().getText()
        expr_symbols = re.findall(r'\b[a-zA-Z_]\w*\b', expr_symbols)
        self.symbol_table.add_dependency([var_name] + expr_symbols, self.current_scope)

        return self.visitChildren(ctx)

    def visitAssignStmt(self, ctx: SimpleLangParser.AssignStmtContext):
        """Procesa asignaciones, registrando dependencias."""
        var_name = ctx.ID().getText()
        expr_symbols = ctx.expr().getText()
        expr_symbols = re.findall(r'\b[a-zA-Z_]\w*\b', expr_symbols)
        #[t.getText() for t in ctx.expr().getTokens(SimpleLangParser.ID)]

        # Registrar variable si no está en la tabla
        if var_name not in self.symbol_table.symbol_table:
            self.symbol_table.add_symbol(var_name, self.current_scope)

        # Registrar dependencia en el hipergrafo
        self.symbol_table.add_dependency([var_name] + expr_symbols, self.current_scope)

        return self.visitChildren(ctx)

    def visitFuncDecl(self, ctx: SimpleLangParser.FuncDeclContext):
        """Procesa declaraciones de funciones."""
        func_name = ctx.ID().getText()
        return_type = ctx.type_().getText()
        params = {}

        # Procesar parámetros
        if ctx.paramList():
            for param in ctx.paramList().param():
                param_name = param.ID().getText()
                param_type = param.type_().getText()
                params[param_name] = param_type

        # Registrar función en la tabla de símbolos
        self.symbol_table.add_function(func_name, self.current_scope, return_type, params)

        # Cambiar de ámbito al cuerpo de la función
        previous_scope = self.current_scope
        self.current_scope = func_name
        self.symbol_table.add_scope(self.current_scope, previous_scope)

        # Procesar el bloque de la función
        self.visit(ctx.block())

        # Regresar al ámbito anterior
        self.current_scope = previous_scope
        return None

    def visitReturnStmt(self, ctx: SimpleLangParser.ReturnStmtContext):
        """Procesa declaraciones de retorno en funciones."""
        if ctx.expr():
            # Extract symbols from the return expression
            return_symbols = [t.getText() for t in ctx.expr().getTokens(SimpleLangParser.ID)]
            # Include the current function (scope) as a dependency source
            self.symbol_table.add_dependency([self.current_scope] + return_symbols, self.current_scope)
        return self.visitChildren(ctx)

    def analyze(self, tree):
        """Ejecuta el análisis semántico recorriendo el árbol."""
        self.visit(tree)

        self.symbol_table.show_forest()
        self.symbol_table.draw_forest()

        self.symbol_table.show_symbol_table()

        self.symbol_table.show_hypergraph()

        self.symbol_table.show_semantic_tree()
        print("Semantic analysis completed.")
        builder = SemanticTreeBuilder(self.symbol_table.forest, self.symbol_table.symbol_table, self.symbol_table.hypergraph)
        semantic_tree_root = builder.build_tree()
        print_semantic_tree(semantic_tree_root)




def print_semantic_tree(node, indent=0):
    indent_space = " " * indent
    loc_info = f" [line: {node.location[0]}, col: {node.location[1]}]" if node.location else ""
    print(f"{indent_space}{node.name} ({node.node_type}, {node.data_type}){loc_info}")
    if node.dependencies:
        print(f"{indent_space}  -> Dependencies: {', '.join(node.dependencies)}")
    for child in node.children:
        print_semantic_tree(child, indent + 4)