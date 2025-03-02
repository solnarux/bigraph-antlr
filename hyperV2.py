import networkx as nx
import matplotlib.pyplot as plt
import re

# Tabla de símbolos con información de variables y sus ámbitos
TablaS =  [
    ["y", "int", "Global", "5"],
    ["x", "int", "Global", "1"],
    ["j", "int", "Global", "x + y"],
    ["myFunc", "fn", "Global", "(int) -> int"],
    ["x", "int", "myFunc", "Parámetro"],
    ["z", "int", "myFunc", "2 + 4"],
    ["h", "int", "myFunc", "x + 2"],
    ["w", "int", "Global", "j * 2"],
    ["f", "int", "myFunc", "h + z"],
    ["a", "int", "myFunc", "x + y + z"]
]

# Crear el grafo de dependencias respetando los scopes y mejorando la jerarquía visual
dep_graph = nx.DiGraph()

# Función para extraer variables de una expresión
def extract_variables(expression):
    return set(re.findall(r'\b[a-zA-Z_]\w*\b', expression))

# Registrar variables en sus respectivos scopes
scope_variables = {}  # Diccionario que mapea scopes a variables
for row in TablaS:
    var_name, _, scope, _ = row
    if scope not in scope_variables:
        scope_variables[scope] = set()
    scope_variables[scope].add(var_name)

# Construcción de aristas de dependencia dentro de los scopes permitidos
for row in TablaS:
    var_name, var_type, scope, expression = row
    dependencies = extract_variables(expression)

    # Filtrar dependencias permitidas (mismo scope o Global)
    valid_dependencies = {dep for dep in dependencies if dep in scope_variables.get(scope, set()) or dep in scope_variables.get("Global", set())}

    # Agregar nodos y aristas al grafo
    if var_type != "fn" and expression != "Parámetro":
        dep_graph.add_node(var_name)
        for dep in valid_dependencies:
            dep_graph.add_edge(dep, var_name)  # Conectar la variable dependiente con sus dependencias

# Generar posiciones jerárquicas corregidas evitando superposiciones
pos = {}
y_step = -2  # Mayor espaciado vertical
x_spacing = 2  # Espaciado horizontal entre nodos
x_offsets = {}  # Almacenar desplazamiento en cada nivel

def assign_dep_position(node, level=0, x_offset=0):
    """ Asigna una posición jerárquica a cada nodo en el grafo de dependencias sin superposición. """
    if node in pos:
        return pos[node][0]  # Evitar re-asignar nodos, devolver coordenada X

    num_children = len(list(dep_graph.successors(node)))
    if level not in x_offsets:
        x_offsets[level] = x_offset
    else:
        x_offsets[level] += x_spacing

    if num_children > 0:
        child_x_positions = [assign_dep_position(child, level + 1, x_offsets[level] + i * x_spacing) 
                             for i, child in enumerate(dep_graph.successors(node))]

        child_x_positions = [x for x in child_x_positions if x is not None]
        center_x = sum(child_x_positions) / len(child_x_positions) if child_x_positions else x_offsets[level]
    else:
        center_x = x_offsets[level]

    pos[node] = (center_x, y_step * level)
    return pos[node][0]

# Asignar posiciones jerárquicas desde los nodos de mayor nivel
for node in list(dep_graph.nodes):
    predecessors = list(dep_graph.predecessors(node))
    if not predecessors:  # Nodo raíz (sin padres)
        assign_dep_position(node, level=0, x_offset=0)

# Ajuste adicional para evitar superposiciones manuales
for node in pos:
    x, y = pos[node]
    pos[node] = (x + (0.5 if "h" in node else 0), y)  # Desplaza 'h' ligeramente a la derecha

# Dibujar el grafo de dependencias con estructura jerárquica mejorada
plt.figure(figsize=(10, 6))
nx.draw(dep_graph, pos, with_labels=True, node_color="lightblue", edge_color="gray", 
        node_size=2500, font_size=10, arrows=True, connectionstyle="arc3,rad=0.1")
plt.show()
