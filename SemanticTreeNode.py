class SemanticTreeNode:
    def __init__(self, name, node_type, data_type=None, value=None, ast_node=None, location=None):
        self.name = name
        self.node_type = node_type      # e.g., 'scope', 'var', 'function', 'param'
        self.data_type = data_type
        self.ast_node = ast_node        # A reference to the AST node
        self.location = location
        self.value = value              # e.g., (line, column)
        self.children = []              # Nested symbols/scopes
        self.dependencies = []          # List of names this node depends on

    def add_child(self, child):
        self.children.append(child)
    
    def add_dependency(self, dependency):
        self.dependencies.append(dependency)

    def __repr__(self):
        return f"<{self.node_type} {self.name} ({self.data_type})>"
