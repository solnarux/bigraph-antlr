import networkx as nx
import hypernetx as hnx
import matplotlib.pyplot as plt

class BigraphSymbolTable:
    def __init__(self):
        # Bosque para representar jerarquía de ámbitos
        self.forest = nx.DiGraph()
        
        # Hipergrafo para representar relaciones semánticas
        self.hypergraph = hnx.Hypergraph({})
        
        # Diccionarios para almacenar información
        self.symbol_table = {}  # Mapeo de identificadores
        self.type_relations = {}  # Relación de símbolos con tipos

    def add_scope(self, scope_name, parent=None):
        """Agrega un nuevo ámbito (nodo en el bosque)."""
        self.forest.add_node(scope_name)
        if parent:
            self.forest.add_edge(parent, scope_name)

    def add_symbol(self, name, scope="global", symbol_type="var", data_type=None):
        """Registra un nuevo símbolo con su tipo y lo agrega al bosque e hipergrafo."""
        full_name = f"{scope}.{name}"
        
        if full_name not in self.symbol_table:
            self.symbol_table[full_name] = {
                "name": name,
                "scope": scope,
                "symbol_type": symbol_type,
                "data_type": data_type
            }
            
            self.forest.add_node(full_name)
            self.forest.add_edge(scope, full_name)
            
            # Relacionar símbolo con su tipo en el hipergrafo
            if data_type:
                type_edge = f"type_{data_type}"
                self.hypergraph.add_edge(type_edge, [full_name, data_type])
                self.type_relations[full_name] = data_type
        
        return full_name
    
    def add_function(self, func_name, scope="global", return_type="void", params=None):
        """Agrega una función y la relaciona con sus parámetros y tipo de retorno."""
        full_func_name = self.add_symbol(func_name, scope, "function", return_type)
        param_names = []

        if params:
            for param_name, param_type in params.items():
                param_full_name = self.add_symbol(param_name, full_func_name, "param", param_type)
                param_names.append(param_full_name)
            
            # Relacionar función con sus parámetros en el hipergrafo
            param_edge = f"params_{func_name}"
            self.hypergraph.add_edge(param_edge, [full_func_name] + param_names)
        
        return full_func_name

    def add_dependency(self, symbols):
        """Agrega una dependencia semántica entre múltiples símbolos en el hipergrafo."""
        nodes = [sym for sym in symbols if sym in self.symbol_table]

        if len(nodes) > 1:
            edge_id = f"dep_{'_'.join(symbols)}"
            self.hypergraph.add_edge(edge_id, nodes)
        else:
            missing = [sym for sym in symbols if sym not in self.symbol_table]
            print(f"⚠️ No se pudo agregar dependencia: {symbols} (faltan: {missing})")

    def show_forest(self):
        """Muestra la estructura jerárquica del bosque."""
        print("\n🌳 Forest (Scopes & Symbols):")
        for scope in nx.topological_sort(self.forest):
            print(f"  {scope} -> {list(self.forest.successors(scope))}")

    def show_hypergraph(self):
        """Muestra la estructura del hipergrafo."""
        print("\n🔗 HYPERGRAPH STRUCTURE\n")
        print("🟢 Nodos en el hipergrafo:")
        for node in self.hypergraph.incidence_dict:
            print(f"   - {node}")

        print("\n🔵 Hiperaristas (Relaciones Semánticas):")
        for edge, nodes in self.hypergraph.incidence_dict.items():
            print(f"   - {edge} conecta: {', '.join(nodes)}")

    def draw_hypergraph(self):
        """Visualiza el hipergrafo con matplotlib."""
        plt.figure(figsize=(6, 6))
        hnx.draw(self.hypergraph)
        plt.show()
