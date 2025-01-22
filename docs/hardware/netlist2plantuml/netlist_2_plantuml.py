import re


def translate_netlist_to_plantuml(netlist_file, output_file):
    # Initialisation du diagramme PlantUML
    plantuml_output = "@startuml\n"

    # Lecture du fichier netlist
    with open(netlist_file, 'r') as f:
        netlist_lines = f.readlines()

    # Expressions régulières pour correspondre aux composants et aux connexions
    component_regex = r'([\w\-\.\+]+)\s+!\s+([\w\-\.\+]+)\s*;\s*(\w+)'
    connection_regex = r'\'([\w\-\.]+)\'\s*;\s*([\w\d]+\.\d+)(?:\s+([\w\d]+\.\d+))*'

    components = {}
    connections = []

    for line in netlist_lines:
        line = line.strip()
        if not line or line.startswith('$'):
            continue  # Ignorer les lignes vides et les directives

        # Correspondance des composants
        component_match = re.match(component_regex, line)
        if component_match:
            component_type, component_name, instance_name = component_match.groups()
            components[instance_name] = (component_type, component_name)

        # Correspondance des connexions
        connection_match = re.match(connection_regex, line)
        if connection_match:
            net_name, *connected_components = connection_match.groups()
            for component in connected_components:
                if component:
                    connections.append((net_name, component))

    # Ajouter les composants à la sortie PlantUML
    for instance_name, (component_type, component_name) in components.items():
        plantuml_output += f'object {instance_name} as {instance_name} <<{component_name}>>\n'

    # Ajouter les connexions à la sortie PlantUML
    for net_name, component in connections:
        if component in components:  # Vérifier que le composant existe
            plantuml_output += f'{net_name} --> {component}\n'

    # Ajouter les connexions d'alimentation explicitement
    plantuml_output += "'-VCC' --> U2.4\n"
    plantuml_output += "'+VCC' --> U2.8\n"

    # End PlantUML diagram
    plantuml_output += "@enduml\n"

    # Écrire dans le fichier de sortie
    with open(output_file, 'w') as f:
        f.write(plantuml_output)


# Exemple d'utilisation
translate_netlist_to_plantuml('netlist.txt', 'output.puml')