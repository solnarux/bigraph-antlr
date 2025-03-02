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
# Reinicializar el grafo para corregir la disposición
scope_tree = nx.DiGraph()

# Agregar nodos para los ámbitos y sus variables con su tipo
for row in TablaS:
    var_name, var_type, scope, content = row

    if var_type != "fn" and content != "Parámetro":
        scope_tree.add_edge(scope, var_name)  # Conectar ámbito con variable
        scope_tree.add_edge(var_name, f"{var_type}: {var_name}")  # Conectar variable con su tipo
        scope_tree.add_edge(f"{var_type}: {var_name}", f"{var_type}: {content}")  # Conectar variable con su tipo

# Generar posiciones jerárquicas corregidas
pos = {}
y_step = -1.5  # Mayor espaciado vertical
x_spacing = 2  # Espaciado horizontal entre nodos
x_offsets = {}  # Almacenar desplazamiento en cada nivel

def assign_position(node, level=0, x_offset=0):
    """ Asigna una posición a cada nodo en la jerarquía con mejor distribución """
    if node in pos:
        return pos[node][0]  # Evitar re-asignar nodos, devolver coordenada X

    num_children = len(list(scope_tree.successors(node)))
    if level not in x_offsets:
        x_offsets[level] = x_offset
    else:
        x_offsets[level] += x_spacing

    if num_children > 0:
        child_x_positions = [assign_position(child, level + 1, x_offsets[level] + i * x_spacing) 
                             for i, child in enumerate(scope_tree.successors(node))]

        child_x_positions = [x for x in child_x_positions if x is not None]
        center_x = sum(child_x_positions) / len(child_x_positions) if child_x_positions else x_offsets[level]
    else:
        center_x = x_offsets[level]

    pos[node] = (center_x, y_step * level)
    return pos[node][0]

# Asignar posiciones desde los nodos raíz "Global" y "myFunc"
for node in list(scope_tree.nodes):
    if node not in pos:
        assign_position(node, level=0, x_offset=0)


# Dibujar el bosque de ámbitos corregido
plt.figure(figsize=(10, 6))
nx.draw(scope_tree, pos, with_labels=True, node_color="lightblue", edge_color="gray", 
        node_size=2500, font_size=10, arrows=True, connectionstyle="arc3,rad=0.1")
plt.show()
