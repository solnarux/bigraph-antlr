import networkx as nx
import hypernetx as hnx
import matplotlib.pyplot as plt

class BigraphSymbolTable:
    def __init__(self):
        # Bosque para representar jerarquía de ámbitos
        self.forest = nx.DiGraph()

        # Hipergrafo para representar relaciones semánticas
        self.hypergraph = hnx.Hypergraph()

        # Diccionario para mapear identificadores a nodos
        self.symbol_table = {}

    def add_scope(self, scope_name, parent=None):
        """Agrega un nuevo ámbito (nodo en el bosque)."""
        self.forest.add_node(scope_name)
        if parent:
            self.forest.add_edge(parent, scope_name)  # Relación jerárquica

    def add_symbol(self, name, scope="global"):
        """Registra un nuevo símbolo en la tabla y lo agrega al bosque."""
        full_name = f"{scope}.{name}"  # Nombre con contexto (ej. global.x)
        
        if full_name not in self.symbol_table:
            self.symbol_table[full_name] = full_name
            self.forest.add_node(full_name)
            self.forest.add_edge(scope, full_name)  # Relación jerárquica
        
        return full_name


    def add_dependency(self, symbols):
        """Agrega una dependencia semántica entre múltiples símbolos (hiperarista)."""
        nodes = [f"global.{sym}" for sym in symbols if f"global.{sym}" in self.symbol_table]

        if len(nodes) == len(symbols):  # Verificamos que todos los símbolos existen
            edge_id = f"dep_{'_'.join(nodes)}"  # ID único para la hiperarista
            self.hypergraph.add_edge(edge_id, nodes)  # Se agrega correctamente la dependencia
        else:
            missing = [sym for sym in symbols if f"global.{sym}" not in self.symbol_table]
            print(f"⚠️ No se pudo agregar dependencia: {symbols} (faltan: {missing})")


    def show_forest(self):
        """Muestra la estructura jerárquica del bosque."""
        print("🌳 Forest (Scopes & Symbols):")
        print(nx.tree_data(self.forest, root=list(self.forest.nodes)[0]))

    def show_hypergraph(self):
        plt.figure(figsize=(6, 6))  # Ajusta el tamaño de la figura
        hnx.draw(self.hypergraph)
        plt.show()

