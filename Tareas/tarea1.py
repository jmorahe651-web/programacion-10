from collections import deque


def dfs_iterativo(grafo, inicio):
    pila = [inicio]
    visitados = set()
    recorrido = []
    
    while pila:
        nodo = pila.pop()
        if nodo in visitados:
            continue
        visitados.add(nodo)
        recorrido.append(nodo)
        
        for vecino in reversed(grafo[nodo]):
            if vecino not in visitados:
                pila.append(vecino)
                
    return recorrido


def ruta_mas_corta(grafo, inicio, destino):
    if inicio == destino:
        return [inicio]
    
    padre = {inicio: None}
    cola = deque([inicio])
    
    while cola:
        nodo = cola.popleft()
        if nodo == destino:
            break
        for vecino in grafo[nodo]:
            if vecino not in padre:
                padre[vecino] = nodo
                cola.append(vecino)
                
    if destino not in padre:
        return None
        
    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = padre[actual]
        
    return ruta[::-1]


def contar_componentes(grafo):
    componente = {}
    cantidad = 0
    
    for inicio in grafo:
        if inicio not in componente:
            cantidad += 1
            componente[inicio] = cantidad
            pila = [inicio]
            
            while pila:
                nodo = pila.pop()
                for vecino in grafo[nodo]:
                    if vecino not in componente:
                        componente[vecino] = cantidad
                        pila.append(vecino)
                        
    return cantidad, componente


def tiene_ciclo(grafo):
    visitados = set()
    
    def dfs_rec(nodo, padre):
        visitados.add(nodo)
        for vecino in grafo[nodo]:
            if vecino == padre:
                continue
            if vecino in visitados:
                return True
            if vecino not in visitados:
                if dfs_rec(vecino, nodo):
                    return True
        return False
        
    for inicio in grafo:
        if inicio not in visitados:
            if dfs_rec(inicio, None):
                return True
    return False


def orden_topologico(grafo):
    nodos = list(grafo.keys())
    entrada = {nodo: 0 for nodo in nodos}
    
    for nodo in grafo:
        for vecino in grafo[nodo]:
            entrada[vecino] += 1
            
    cola = deque([nodo for nodo in nodos if entrada[nodo] == 0])
    orden = []
    
    while cola:
        nodo = cola.popleft()
        orden.append(nodo)
        for vecino in grafo[nodo]:
            entrada[vecino] -= 1
            if entrada[vecino] == 0:
                cola.append(vecino)
                
    return orden




def main():

    red_vial = {
        "Santiago": ["Mercedes Sur", "Barbacoas", "Candelarita"],
        "Mercedes Sur": ["Santiago", "San Rafael"],
        "Barbacoas": ["Santiago", "Grifo Alto"],
        "San Rafael": ["Mercedes Sur", "Grifo Alto"],
        "Grifo Alto": ["Barbacoas", "San Rafael"],
        "Candelarita": ["Santiago"],
        "Desamparaditos": ["Chires"],
        "Chires": ["Desamparaditos"],
        "Zapatón": []
    }

    plan_obras = {
        "Estudio": ["Permisos", "Materiales"],
        "Permisos": ["Excavación"],
        "Materiales": ["Alcantarillado", "Asfaltado"],
        "Excavación": ["Alcantarillado"],
        "Alcantarillado": ["Asfaltado"],
        "Asfaltado": ["Señalización"],
        "Señalización": []
    }

    while True:
        print("\n=== RED VIAL DE PURISCAL ===")
        print("1. Ver la red de caminos")
        print("2. Agregar un camino")
        print("3. Comunidades alcanzables desde una comunidad")
        print("4. Ruta con menos tramos entre dos comunidades")
        print("5. Componentes conexas de la red")
        print("6. Detectar caminos circulares")
        print("7. Orden de ejecución de las obras")
        print("8. Agregar un prerrequisito entre obras")
        print("9. Salir")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\nRed de caminos de Puriscal")
            suma_grados = 0
            for comunidad, vecinos in red_vial.items():
                grado = len(vecinos)
                suma_grados += grado
                vecinos_str = ", ".join(vecinos) if vecinos else "sin caminos"
                print(f"{comunidad} (Grado: {grado}): {vecinos_str}")
            total_caminos = suma_grados // 2
            print(f"Total de caminos en la red: {total_caminos}")

        elif opcion == "2":
            c1 = input("Primera comunidad: ").strip().title()
            c2 = input("Segunda comunidad: ").strip().title()
            
            if c1 not in red_vial and c2 not in red_vial:
                print(f"No existen las comunidades '{c1}' y '{c2}'.")
            elif c1 not in red_vial:
                print(f"No existe la comunidad '{c1}'.")
            elif c2 not in red_vial:
                print(f"No existe la comunidad '{c2}'.")
            elif c1 == c2:
                print("Una comunidad no puede conectarse consigo misma.")
            elif c2 in red_vial[c1]:
                print(f"Ya existe un camino entre {c1} y {c2}.")
            else:
                red_vial[c1].append(c2)
                red_vial[c2].append(c1)
                print(f"Camino agregado entre {c1} y {c2}!")

        elif opcion == "3":
            inicio = input("Comunidad de inicio: ").strip().title()
            
            if inicio not in red_vial:
                print(f"No existe la comunidad '{inicio}'.")
            else:
                resultado = dfs_iterativo(red_vial, inicio)
                print(f"Comunidades alcanzables desde {inicio}: {len(resultado)}")
                print(" -> ".join(resultado))

        elif opcion == "4":
            origen = input("Comunidad de origen: ").strip().title()
            destino = input("Comunidad de destino: ").strip().title()
            
            if origen not in red_vial or destino not in red_vial:
                no_encontrada = origen if origen not in red_vial else destino
                print(f"No existe la comunidad '{no_encontrada}'.")
            elif origen == destino:
                print("El origen y el destino no pueden ser la misma comunidad.")
            else:
                ruta = ruta_mas_corta(red_vial, origen, destino)
                if ruta is None:
                    print(f"No existe una ruta entre {origen} y {destino}.")
                else:
                    tramos = len(ruta) - 1
                    print("Ruta con menos tramos:", " -> ".join(ruta))
                    print(f"Cantidad de tramos: {tramos}")

        elif opcion == "5":
            cantidad, diccionario_comp = contar_componentes(red_vial)
            
            comps = {}
            for comunidad in red_vial:
                num_comp = diccionario_comp[comunidad]
                if num_comp not in comps:
                    comps[num_comp] = []
                comps[num_comp].append(comunidad)
                
            for num, miembros in comps.items():
                print(f"Componente {num}: {', '.join(miembros)}")
                
            if cantidad == 1:
                print(f"La red tiene {cantidad} componente conexa y todas las comunidades están comunicadas.")
            else:
                print(f"La red tiene {cantidad} componentes conexas y no todas las comunidades están comunicadas.")

        elif opcion == "6":
            ciclo_detectado = tiene_ciclo(red_vial)
            V = len(red_vial)
            c, _ = contar_componentes(red_vial)
            suma_grados = sum(len(vecinos) for vecinos in red_vial.values())
            E = suma_grados // 2
            max_aristas_sin_ciclo = V - c
            conteo_con_ciclo = E > max_aristas_sin_ciclo
            
            if ciclo_detectado:
                print("Búsqueda con DFS: la red tiene al menos un camino circular.")
            else:
                print("Búsqueda con DFS: la red no tiene caminos circulares.")
                
            print(f"Comprobación por conteo: {E} caminos frente a {max_aristas_sin_ciclo} permitidos sin ciclos ({V} comunidades - {c} componentes).")
            
            if ciclo_detectado == conteo_con_ciclo:
                print("Los dos métodos coinciden.")
            else:
                print("Los métodos difieren.")

        elif opcion == "7":
            orden = orden_topologico(plan_obras)
            if len(orden) == len(plan_obras):
                print("Orden de ejecución de las obras:")
                print(" -> ".join(orden))
            else:
                print("Hay un ciclo de prerrequisitos: no existe un orden válido.")
                bloqueadas = [obra for obra in plan_obras if obra not in orden]
                print("Obras bloqueadas:", ", ".join(bloqueadas))

        elif opcion == "8":
            previa = input("Obra previa: ").strip().title()
            dependiente = input("Obra que depende de ella: ").strip().title()
            
            if previa not in plan_obras or dependiente not in plan_obras:
                print("Error: Una o ambas obras no existen en el plan.")
            elif previa == dependiente:
                print("Error: Una obra no puede depender de sí misma.")
            elif dependiente in plan_obras[previa]:
                print(f"El prerrequisito entre {previa} y {dependiente} ya existe.")
            else:
                plan_obras[previa].append(dependiente)
                print(f"Prerrequisito agregado: {previa} debe terminar antes de {dependiente}.")

        elif opcion == "9":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Debe digitar un número del 1 al 9.")

            
if __name__ == "__main__":
    main()