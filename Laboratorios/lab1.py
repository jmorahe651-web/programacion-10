NOMBRES_ESPACIOS = {
    "E": "Entrada",
    "C": "Exposición de ciencias",
    "J": "Zona de juegos",
    "R": "Robótica",
    "T": "Talleres",
    "S": "Salida",
}

nodos = ["E", "C", "J", "R", "T", "S"]

mapa = {
    "E": ["C", "J"],
    "C": ["E", "R", "T"],
    "J": ["E", "S"],
    "R": ["C", "S"],
    "T": ["C", "S"],
    "S": ["J", "R", "T"],
}




def construir_matriz(mapa, nodos):
    """Construye una matriz de adyacencia dinámica a partir del diccionario mapa."""
    matriz = []
    for origen in nodos:
        fila = []
        for destino in nodos:
            if destino in mapa[origen]:
                fila.append(1)
            else:
                fila.append(0)
        matriz.append(fila)
    return matriz


def dfs_recursivo(mapa, inicio):
    """Recorrido en profundidad recursivo."""
    recorrido = []
    visitados = set()

    def explorar(nodo):
        visitados.add(nodo)
        recorrido.append(nodo)

        for vecino in mapa[nodo]:
            if vecino not in visitados:
                explorar(vecino)

    explorar(inicio)
    return recorrido


def dfs_iterativo(mapa, inicio):
    pila = [inicio]
    visitados = set()
    recorrido = []

    while pila:
        nodo = pila.pop()
        if nodo in visitados:
            continue

        visitados.add(nodo)
        recorrido.append(nodo)

        for vecino in reversed(mapa[nodo]):
            if vecino not in visitados:
                pila.append(vecino)

    return recorrido


def solicitar_nodo_valido(mensaje):
    while True:
        nodo = input(mensaje).strip().upper()
        if nodo in mapa:
            return nodo
        print("Ese espacio no existe en el mapa.")




def main():
    while True:
        print("\n=== MAPA DE LA FERIA CIENTÍFICA ===")
        print("1. Ver conexiones de un espacio")
        print("2. Ver matriz de adyacencia")
        print("3. Recorrer con DFS recursivo")
        print("4. Recorrer con DFS iterativo")
        print("5. Consultar si hay un pasillo directo")
        print("6. Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            nodo = solicitar_nodo_valido("Espacio: ")
            nombre_completo = NOMBRES_ESPACIOS[nodo]
            vecinos_str = ", ".join(mapa[nodo])
            print(f"{nodo} · {nombre_completo} se conecta con: {vecinos_str}")

        elif opcion == "2":
            matriz = construir_matriz(mapa, nodos)
            print("\n  " + " ".join(nodos))
            for i, fila in enumerate(matriz):
                fila_str = " ".join(str(val) for val in fila)
                print(f"{nodos[i]} {fila_str}")

        elif opcion == "3":
            inicio = solicitar_nodo_valido("Punto de inicio: ")
            resultado = dfs_recursivo(mapa, inicio)
            print(" -> ".join(resultado))

        elif opcion == "4":
            inicio = solicitar_nodo_valido("Punto de inicio: ")
            resultado = dfs_iterativo(mapa, inicio)
            print(" -> ".join(resultado))

        elif opcion == "5":
            origen = solicitar_nodo_valido("Espacio de origen: ")
            destino = solicitar_nodo_valido("Espacio de destino: ")

            matriz = construir_matriz(mapa, nodos)
            fila_idx = nodos.index(origen)
            col_idx = nodos.index(destino)
            
            if matriz[fila_idx][col_idx] == 1:
                print(
                    f"Existe un pasillo directo entre {origen} ({NOMBRES_ESPACIOS[origen]}) y {destino} ({NOMBRES_ESPACIOS[destino]})."
                )
            else:
                print(
                    f"No existe un pasillo directo entre {origen} ({NOMBRES_ESPACIOS[origen]}) y {destino} ({NOMBRES_ESPACIOS[destino]})."
                )

        elif opcion == "6":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Ingrese un número entre 1 y 6.")


if __name__ == "__main__":
    main()
