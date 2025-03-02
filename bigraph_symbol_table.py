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

    def add_symbol(self, name, scope="global", symbol_type="var",  data_type=None, value=None, ast_node=None, location=None):
        """Registra un nuevo símbolo con su tipo y lo agrega al bosque e hipergrafo."""
        full_name = f"{scope}.{name}"
        if full_name not in self.symbol_table:
            self.symbol_table[full_name] = {
                "name": name,
                "scope": scope,
                "symbol_type": symbol_type,
                "data_type": data_type,
                "ast_node": ast_node,
                "location": location,
                "value": value
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

    def resolve_symbol(self, symbol, current_scope):
        candidate = f"{current_scope}.{symbol}"
        if candidate in self.symbol_table:
            return candidate
        candidate = f"global.{symbol}"
        if candidate in self.symbol_table:
            return candidate
        candidate = f"global.{current_scope}.{symbol}"
        if candidate in self.symbol_table:
            return candidate
        return None

    def add_dependency(self, symbols, current_scope="global"):
        # Attempt to resolve each symbol into its fully qualified version
        resolved_nodes = []
        for sym in symbols:
            full_sym = sym if sym in self.symbol_table else self.resolve_symbol(sym, current_scope)
            if full_sym:
                resolved_nodes.append(full_sym)
            else:
                print(f"⚠️ Symbol '{sym}' could not be resolved (in scope {current_scope}).")
        if len(resolved_nodes) >1:
            edge_id = f"dep_{'_'.join(symbols)}"
            # self.hypergraph.add_edge(edge_id, resolved_nodes)
            self.hypergraph.add_edge(edge_id)
            # Add incidences (connections between edge and nodes)
            for node in resolved_nodes:
                self.hypergraph.add_incidence(edge_id, node)

    def show_forest(self):
        """Muestra la estructura jerárquica del bosque."""
        print("\n🌳 Forest (Scopes & Symbols):")
        for scope in nx.topological_sort(self.forest):
            print(f"  {scope} -> {list(self.forest.successors(scope))}")

    def draw_forest(self):
        """Visualizes the forest of scopes using a top-down hierarchical layout with space-around spacing."""
        plt.figure(figsize=(10, 8))

        # Compute hierarchical positions
        pos = self.hierarchical_pos(self.forest)

        # Draw the graph with the computed hierarchical layout
        nx.draw(self.forest, pos, with_labels=True, arrows=True, 
                node_size=2000, node_color="skyblue", font_size=10, edge_color="gray")

        plt.title("Bigraph Symbol Table - Scope Hierarchy (Space-Around)")
        plt.show()

    def hierarchical_pos(self, G, root=None, width=1., vert_gap=0.2, xcenter=0.5):
        """Computes hierarchical positions for a directed graph."""
        pos = self._hierarchy_pos(G, root, width, vert_gap, xcenter)
        return pos
    
    def _hierarchy_pos(self, G, root=None, width=1., vert_gap=0.2, xcenter=0.5, pos=None, parent=None, level=0, visited=None):
        """Recursively assigns positions for nodes in a hierarchical layout with space-around spacing."""
        if pos is None:
            pos = {}
        if visited is None:
            visited = set()

        if root is None:
            root = [n for n, d in G.in_degree() if d == 0][0]  # Find root if not given

        if root in visited:  # Prevent re-positioning already placed nodes
            return pos
        visited.add(root)

        pos[root] = (xcenter, 1 - level * vert_gap)

        children = list(G.successors(root))
        num_children = len(children)

        if num_children != 0:
            # Calculate the spacing between children
            if num_children == 1:
                dx = 0  # No spacing needed for a single child
            else:
                dx = width / (num_children - 1)  # Space-around spacing

            # Start from the leftmost position
            next_x = xcenter - width / 2

            for child in children:
                # If a node has multiple parents, don't override its position
                if child not in pos:
                    pos[child] = (next_x, 1 - (level + 1) * vert_gap)
                # Recursively compute positions for children
                self._hierarchy_pos(G, child, width=width, vert_gap=vert_gap, 
                                    xcenter=next_x, pos=pos, parent=root, level=level + 1, visited=visited)
                next_x += dx  # Move right for next child

        return pos

    def show_hypergraph(self):
        """Muestra la estructura del hipergrafo."""
        print("\n🔗 HYPERGRAPH STRUCTURE\n")

        print("\n🔵 Hiperaristas (Relaciones Semánticas):")
        for edge, nodes in self.hypergraph.incidence_dict.items():
            print(f"   - {edge} conecta: {', '.join(nodes)}")        

    def show_semantic_tree(self):
        """Prints an enhanced version of the forest with dependencies."""
        print("\n🌳 SEMANTIC TREE\n")

        # First, print the scope-based structure (forest)
        for scope in nx.topological_sort(self.forest):
            indent_level = scope.count(".") * 2  # Adjust indentation based on scope depth
            print(" " * indent_level + f"📂 {scope}")

            # Find symbols in this scope
            for symbol in self.forest.successors(scope):
                if symbol in self.symbol_table:
                    symbol_info = self.symbol_table[symbol]
                    symbol_type = symbol_info["symbol_type"]
                    data_type = symbol_info["data_type"] or "unknown"
                    symbol_value = symbol_info["value"] or "unknown"

                    print(" " * (indent_level + 2) + f"📌 {symbol} ({symbol_type}: {data_type}, value: {symbol_value})")


                    # Find dependencies related to this symbol
                    for edge, nodes in self.hypergraph.incidence_dict.items():
                        if symbol in nodes:
                            dep_nodes = [n for n in nodes if n != symbol]
                            if dep_nodes:
                                print(" " * (indent_level + 4) + f"🔗 Depends on: {', '.join(dep_nodes)}")

    def show_symbol_table(self):
        """Muestra la tabla de símbolos de manera legible."""
        print("\n📋 SYMBOL TABLE\n")
        for full_name, info in self.symbol_table.items():
            print(f"🔹 {full_name}")
            for key, value in info.items():
                print(f"   - {key}: {value}")

    def draw_hypergraph(self):
        """Visualizes the hypergraph using a directed graph (DiGraph) representation, including all nodes."""
        # Create a copy of the forest (DiGraph) to represent the hypergraph
        hypergraph_digraph = nx.DiGraph()

        # Add all nodes from the forest (even those without connections)
        for node in self.forest.nodes:
            hypergraph_digraph.add_node(node)

        # Add nodes and hyperedges from the hypergraph
        for edge, nodes in self.hypergraph.incidence_dict.items():
            # Add the hyperedge as a central node
            hypergraph_digraph.add_node(edge, type="hyperedge")
            # Connect the hyperedge to its constituent nodes
            for node in nodes:
                hypergraph_digraph.add_edge(edge, node)

        # Compute positions for the nodes
        pos = nx.spring_layout(hypergraph_digraph)

        # Draw the graph
        plt.figure(figsize=(12, 8))

        # Draw nodes
        node_colors = []
        for node in hypergraph_digraph.nodes:
            if hypergraph_digraph.nodes[node].get("type") == "hyperedge":
                node_colors.append("red")  # Color hyperedges differently
            else:
                node_colors.append("skyblue")

        nx.draw(hypergraph_digraph, pos, with_labels=True, node_color=node_colors, 
                node_size=2000, font_size=10, edge_color="gray", arrows=False)

        plt.title("Hypergraph Representation using DiGraph (All Nodes Included)")
        plt.show()
