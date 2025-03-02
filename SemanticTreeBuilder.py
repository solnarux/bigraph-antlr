from SemanticTreeNode import SemanticTreeNode

class SemanticTreeBuilder:
    def __init__(self, forest, symbol_table, hypergraph):
        self.forest = forest
        self.symbol_table = symbol_table  # The dictionary of symbols
        self.hypergraph = hypergraph      # The hypergraph of dependencies
        self.node_map = {}  # Maps full names to SemanticTreeNode objects

    def build_tree(self):
        # Start with the global scope as root
        root = self._build_node("global")
        self._attach_children(root)
        self._annotate_dependencies()
        return root

    def _build_node(self, full_name):
        # Retrieve the stored symbol information if it exists,
        # otherwise treat it as a scope node.
        info = self.symbol_table.get(full_name, {"name": full_name, "symbol_type": "scope"})
        node = SemanticTreeNode(
            name=full_name,
            node_type=info.get("symbol_type", "scope"),
            data_type=info.get("data_type"),
            ast_node=info.get("ast_node"),
            location=info.get("location")
        )
        self.node_map[full_name] = node
        return node

    def _attach_children(self, parent_node):
        # For every edge from the parent in the forest, create child nodes.
        for child in self.forest.successors(parent_node.name):
            child_node = self._build_node(child)
            parent_node.add_child(child_node)
            self._attach_children(child_node)

    def _annotate_dependencies(self):
        # For each hypergraph edge, annotate the involved SemanticTreeNodes.
        for edge, nodes in self.hypergraph.incidence_dict.items():
            # Each edge connects multiple nodes, so add dependencies among them.
            for node in nodes:
                # Use the node map to retrieve the SemanticTreeNode
                if node in self.node_map:
                    # Add all other nodes in this hyperedge as dependencies.
                    deps = [n for n in nodes if n != node and n in self.node_map]
                    for dep in deps:
                        self.node_map[node].add_dependency(dep)
