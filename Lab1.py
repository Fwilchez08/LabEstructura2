from typing import Optional, List

class Nodo:
    """
    Clase que representa un nodo del árbol AVL
    Cada nodo contiene información de un país y su temperatura medias
    """
    def __init__(self, iso3: str, pais: str, temperatura_media: float):
        self.iso3 = iso3  # Código ISO3 del país
        self.pais = pais  # Nombre completo del país
        self.temperatura_media = temperatura_media  # Métrica para comparación
        self.altura = 1  # Altura del nodo en el árbol
        self.izquierdo: Optional['Nodo'] = None  # Hijo izquierdo
        self.derecho: Optional['Nodo'] = None  # Hijo derecho
        self.padre: Optional['Nodo'] = None  # Referencia al padre

    def __str__(self):
        return f"{self.iso3} ({self.temperatura_media}°C)"

class ArbolAVL:
    """
    Implementación de un árbol AVL (auto-balanceado)
    Utiliza la temperatura media como métrica de comparación
    """

    def __init__(self):
        self.raiz: Optional[Nodo] = None
        self.nodos_almacenados: List[Nodo] = []  # Para operaciones de búsqueda globales

    def obtener_altura(self, nodo: Optional[Nodo]) -> int:
        """Obtiene la altura de un nodo"""
        if not nodo:
            return 0
        return nodo.altura

    def obtener_factor_balance(self, nodo: Optional[Nodo]) -> int:
        """Calcula el factor de balance de un nodo"""
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierdo) - self.obtener_altura(nodo.derecho)

    def actualizar_altura(self, nodo: Nodo):
        """Actualiza la altura de un nodo basándose en sus hijos"""
        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierdo),
                             self.obtener_altura(nodo.derecho))

    def rotar_derecha(self, y: Nodo) -> Nodo:
        """Realiza una rotación a la derecha"""
        x = y.izquierdo
        T2 = x.derecho

        # Realizar rotación
        x.derecho = y
        y.izquierdo = T2

        # Actualizar padres
        x.padre = y.padre
        y.padre = x
        if T2:
            T2.padre = y

        # Actualizar alturas
        self.actualizar_altura(y)
        self.actualizar_altura(x)

        return x

    def rotar_izquierda(self, x: Nodo) -> Nodo:
        """Realiza una rotación a la izquierda"""
        y = x.derecho
        T2 = y.izquierdo

        # Realizar rotación
        y.izquierdo = x
        x.derecho = T2

        # Actualizar padres
        y.padre = x.padre
        x.padre = y
        if T2:
            T2.padre = x

        # Actualizar alturas
        self.actualizar_altura(x)
        self.actualizar_altura(y)

        return y

    def insertar(self, iso3: str, pais: str, temperatura_media: float) -> bool:
        """Inserta un nuevo nodo en el árbol"""
        try:
            self.raiz = self._insertar_recursivo(self.raiz, iso3, pais, temperatura_media)
            return True
        except Exception as e:
            print(f"Error al insertar: {e}")
            return False

    def _insertar_recursivo(self, nodo: Optional[Nodo], iso3: str, pais: str, temperatura_media: float) -> Nodo:
        """Función recursiva para insertar un nodo"""
        # Inserción normal de BST
        if not nodo:
            nuevo_nodo = Nodo(iso3, pais, temperatura_media)
            self.nodos_almacenados.append(nuevo_nodo)
            return nuevo_nodo

        if temperatura_media < nodo.temperatura_media:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, iso3, pais, temperatura_media)
            nodo.izquierdo.padre = nodo
        elif temperatura_media > nodo.temperatura_media:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, iso3, pais, temperatura_media)
            nodo.derecho.padre = nodo
        else:
            # Temperaturas iguales, no insertar duplicados
            raise ValueError(f"Ya existe un país con temperatura media {temperatura_media}°C")

        # Actualizar altura del nodo actual
        self.actualizar_altura(nodo)

        # Obtener factor de balance
        balance = self.obtener_factor_balance(nodo)

        # Casos de rotación
        # Caso Izquierda-Izquierda
        if balance > 1 and temperatura_media < nodo.izquierdo.temperatura_media:
            return self.rotar_derecha(nodo)

        # Caso Derecha-Derecha
        if balance < -1 and temperatura_media > nodo.derecho.temperatura_media:
            return self.rotar_izquierda(nodo)

        # Caso Izquierda-Derecha
        if balance > 1 and temperatura_media > nodo.izquierdo.temperatura_media:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)

        # Caso Derecha-Izquierda
        if balance < -1 and temperatura_media < nodo.derecho.temperatura_media:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)

        return nodo

    def buscar(self, temperatura_media: float) -> Optional[Nodo]:
        """Busca un nodo por su temperatura media"""
        return self._buscar_recursivo(self.raiz, temperatura_media)

    def _buscar_recursivo(self, nodo: Optional[Nodo], temperatura_media: float) -> Optional[Nodo]:
        """Función recursiva para buscar un nodo"""
        if not nodo or abs(nodo.temperatura_media - temperatura_media) < 0.001:  # Tolerancia para floats
            return nodo

        if temperatura_media < nodo.temperatura_media:
            return self._buscar_recursivo(nodo.izquierdo, temperatura_media)
        else:
            return self._buscar_recursivo(nodo.derecho, temperatura_media)

    def eliminar(self, temperatura_media: float) -> bool:
        """Elimina un nodo del árbol usando la métrica dada"""
        try:
            nodo_a_eliminar = self.buscar(temperatura_media)
            if not nodo_a_eliminar:
                return False

            # Remover de la lista de nodos almacenados
            if nodo_a_eliminar in self.nodos_almacenados:
                self.nodos_almacenados.remove(nodo_a_eliminar)

            self.raiz = self._eliminar_recursivo(self.raiz, temperatura_media)
            return True
        except Exception as e:
            print(f"Error al eliminar: {e}")
            return False

    def _eliminar_recursivo(self, nodo: Optional[Nodo], temperatura_media: float) -> Optional[Nodo]:
        """Función recursiva para eliminar un nodo"""
        if not nodo:
            return nodo

        # Buscar el nodo a eliminar
        if temperatura_media < nodo.temperatura_media:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, temperatura_media)
        elif temperatura_media > nodo.temperatura_media:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, temperatura_media)
        else:
            # Nodo encontrado, proceder con eliminación
            if not nodo.izquierdo or not nodo.derecho:
                temp = nodo.izquierdo if nodo.izquierdo else nodo.derecho

                if not temp:  # Nodo sin hijos
                    temp = nodo
                    nodo = None
                else:  # Nodo con un hijo
                    nodo.iso3 = temp.iso3
                    nodo.pais = temp.pais
                    nodo.temperatura_media = temp.temperatura_media
                    # Actualizar referencias padre
                    if nodo.izquierdo:
                        nodo.izquierdo.padre = nodo
                    if nodo.derecho:
                        nodo.derecho.padre = nodo
            else:
                # Nodo con dos hijos
                temp = self._obtener_minimo(nodo.derecho)

                # Copiar datos del sucesor inorden
                nodo.iso3 = temp.iso3
                nodo.pais = temp.pais
                nodo.temperatura_media = temp.temperatura_media

                # Eliminar el sucesor inorden
                nodo.derecho = self._eliminar_recursivo(nodo.derecho, temp.temperatura_media)

        if not nodo:
            return nodo

        # Actualizar altura
        self.actualizar_altura(nodo)

        # Obtener factor de balance
        balance = self.obtener_factor_balance(nodo)

        # Rotaciones para rebalancear
        # Caso Izquierda-Izquierda
        if balance > 1 and self.obtener_factor_balance(nodo.izquierdo) >= 0:
            return self.rotar_derecha(nodo)

        # Caso Izquierda-Derecha
        if balance > 1 and self.obtener_factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)

        # Caso Derecha-Derecha
        if balance < -1 and self.obtener_factor_balance(nodo.derecho) <= 0:
            return self.rotar_izquierda(nodo)

        # Caso Derecha-Izquierda
        if balance < -1 and self.obtener_factor_balance(nodo.derecho) > 0:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)

        return nodo

    def _obtener_minimo(self, nodo: Nodo) -> Nodo:
        """Obtiene el nodo con el valor mínimo en el subárbol"""
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return nodo

    def buscar_mayor_promedio_global(self, temperatura_limite: float) -> List[Nodo]:
        """Busca nodos con temperatura mayor o igual a un valor dado"""
        resultado = []
        for nodo in self.nodos_almacenados:
            if nodo.temperatura_media >= temperatura_limite:
                resultado.append(nodo)
        return resultado

    def recorrido_por_niveles(self) -> List[List[str]]:
        """Recorrido por niveles del árbol (BFS) - Versión recursiva"""
        if not self.raiz:
            return []

        resultado = []
        altura_maxima = self.obtener_altura(self.raiz)

        for nivel in range(1, altura_maxima + 1):
            nodos_nivel = []
            self._obtener_nivel_recursivo(self.raiz, nivel, 1, nodos_nivel)
            if nodos_nivel:
                resultado.append(nodos_nivel)

        return resultado

    def _obtener_nivel_recursivo(self, nodo: Optional[Nodo], nivel_objetivo: int, nivel_actual: int, resultado: List[str]):
        """Función recursiva para obtener nodos de un nivel específico"""
        if not nodo:
            return

        if nivel_actual == nivel_objetivo:
            resultado.append(nodo.iso3)
        elif nivel_actual < nivel_objetivo:
            self._obtener_nivel_recursivo(nodo.izquierdo, nivel_objetivo, nivel_actual + 1, resultado)
            self._obtener_nivel_recursivo(nodo.derecho, nivel_objetivo, nivel_actual + 1, resultado)

    def obtener_nivel_nodo(self, nodo: Nodo) -> int:
        """Obtiene el nivel de un nodo específico"""
        return self._calcular_nivel(self.raiz, nodo.temperatura_media, 1)

    def _calcular_nivel(self, nodo_actual: Optional[Nodo], temperatura_objetivo: float, nivel: int) -> int:
        """Calcula el nivel de un nodo recursivamente"""
        if not nodo_actual:
            return -1

        if abs(nodo_actual.temperatura_media - temperatura_objetivo) < 0.001:
            return nivel

        if temperatura_objetivo < nodo_actual.temperatura_media:
            return self._calcular_nivel(nodo_actual.izquierdo, temperatura_objetivo, nivel + 1)
        else:
            return self._calcular_nivel(nodo_actual.derecho, temperatura_objetivo, nivel + 1)

    def obtener_padre(self, nodo: Nodo) -> Optional[Nodo]:
        """Obtiene el padre de un nodo"""
        return nodo.padre

    def obtener_abuelo(self, nodo: Nodo) -> Optional[Nodo]:
        """Obtiene el abuelo de un nodo"""
        if nodo.padre and nodo.padre.padre:
            return nodo.padre.padre
        return None

    def obtener_tio(self, nodo: Nodo) -> Optional[Nodo]:
        """Obtiene el tío de un nodo"""
        abuelo = self.obtener_abuelo(nodo)
        if not abuelo:
            return None

        if nodo.padre == abuelo.izquierdo:
            return abuelo.derecho
        else:
            return abuelo.izquierdo

    def mostrar_arbol_simple(self):
        """Muestra una representación simple del árbol"""
        if not self.raiz:
            print("El árbol está vacío")
            return

        print("\n=== ESTRUCTURA DEL ÁRBOL ===")
        self._mostrar_arbol_recursivo(self.raiz, "", True)

    def _mostrar_arbol_recursivo(self, nodo: Optional[Nodo], prefijo: str, es_ultimo: bool):
        """Función recursiva para mostrar el árbol"""
        if not nodo:
            return

        print(f"{prefijo}{'└── ' if es_ultimo else '├── '}{nodo.iso3} ({nodo.temperatura_media}°C)")

        if nodo.izquierdo or nodo.derecho:
            if nodo.derecho:
                self._mostrar_arbol_recursivo(nodo.derecho,
                                            f"{prefijo}{'    ' if es_ultimo else '│   '}",
                                            not nodo.izquierdo)
            if nodo.izquierdo:
                self._mostrar_arbol_recursivo(nodo.izquierdo,
                                            f"{prefijo}{'    ' if es_ultimo else '│   '}",
                                            True)

def mostrar_menu():
    """Muestra el menú principal del programa"""
    print("\n" + "="*50)
    print("  LABORATORIO AVL - ESTRUCTURA DE DATOS II")
    print("="*50)
    print("1.  Insertar nodo")
    print("2.  Eliminar nodo")
    print("3.  Buscar nodo")
    print("4.  Buscar nodos con temperatura >= valor")
    print("5.  Mostrar recorrido por niveles")
    print("6.  Mostrar árbol")
    print("7.  Operaciones con nodo seleccionado")
    print("8.  Salir")
    print("="*50)

def operaciones_nodo(arbol: ArbolAVL, nodo: Nodo):
    """Submenú para operaciones específicas con un nodo"""
    while True:
        print(f"\n=== OPERACIONES CON NODO: {nodo.iso3} ===")
        print(f"País: {nodo.pais}")
        print(f"Temperatura media: {nodo.temperatura_media}°C")
        print("\n1. Obtener nivel del nodo")
        print("2. Obtener factor de balanceo")
        print("3. Encontrar padre")
        print("4. Encontrar abuelo")
        print("5. Encontrar tío")
        print("6. Volver al menú principal")

        try:
            opcion = int(input("\nSeleccione una opción: "))

            if opcion == 1:
                nivel = arbol.obtener_nivel_nodo(nodo)
                print(f"Nivel del nodo {nodo.iso3}: {nivel}")

            elif opcion == 2:
                factor = arbol.obtener_factor_balance(nodo)
                print(f"Factor de balanceo del nodo {nodo.iso3}: {factor}")

            elif opcion == 3:
                padre = arbol.obtener_padre(nodo)
                if padre:
                    print(f"Padre de {nodo.iso3}: {padre.iso3} ({padre.temperatura_media}°C)")
                else:
                    print(f"El nodo {nodo.iso3} es la raíz (no tiene padre)")

            elif opcion == 4:
                abuelo = arbol.obtener_abuelo(nodo)
                if abuelo:
                    print(f"Abuelo de {nodo.iso3}: {abuelo.iso3} ({abuelo.temperatura_media}°C)")
                else:
                    print(f"El nodo {nodo.iso3} no tiene abuelo")

            elif opcion == 5:
                tio = arbol.obtener_tio(nodo)
                if tio:
                    print(f"Tío de {nodo.iso3}: {tio.iso3} ({tio.temperatura_media}°C)")
                else:
                    print(f"El nodo {nodo.iso3} no tiene tío")

            elif opcion == 6:
                break

            else:
                print("Opción inválida")

            input("\nPresione Enter para continuar...")

        except ValueError:
            print("Error: Ingrese un número válido")
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Función principal del programa"""
    arbol = ArbolAVL()

    # Datos de ejemplo para pruebas rápidas
    paises_ejemplo = [
        ("COL", "Colombia", 24.5),
        ("USA", "Estados Unidos", 12.8),
        ("BRA", "Brasil", 26.2),
        ("CAN", "Canadá", 3.7),
        ("MEX", "México", 21.4),
        ("ARG", "Argentina", 14.9),
        ("CHI", "Chile", 11.2),
        ("FRA", "Francia", 11.8),
        ("ESP", "España", 15.6),
        ("JPN", "Japón", 16.1)
    ]

    print("¡Bienvenido al Laboratorio de Árbol AVL!")
    print("\n¿Desea cargar datos de ejemplo? (s/n): ", end="")
    if input().lower() == 's':
        print("\nCargando datos de ejemplo...")
        for iso3, pais, temp in paises_ejemplo:
            arbol.insertar(iso3, pais, temp)
        print(f"Se han cargado {len(paises_ejemplo)} países de ejemplo")

    while True:
        mostrar_menu()

        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:  # Insertar nodo
                print("\n=== INSERTAR NODO ===")
                iso3 = input("Código ISO3 del país: ").upper()
                pais = input("Nombre del país: ")
                temperatura = float(input("Temperatura media (°C): "))

                if arbol.insertar(iso3, pais, temperatura):
                    print(f"✓ País {iso3} insertado correctamente")
                    arbol.mostrar_arbol_simple()
                else:
                    print("✗ Error al insertar el país")

            elif opcion == 2:  # Eliminar nodo
                print("\n=== ELIMINAR NODO ===")
                temperatura = float(input("Temperatura media del país a eliminar: "))

                nodo = arbol.buscar(temperatura)
                if nodo:
                    print(f"País encontrado: {nodo.iso3} - {nodo.pais}")
                    confirmar = input("¿Confirma la eliminación? (s/n): ")
                    if confirmar.lower() == 's':
                        if arbol.eliminar(temperatura):
                            print("✓ País eliminado correctamente")
                            arbol.mostrar_arbol_simple()
                        else:
                            print("✗ Error al eliminar el país")
                    else:
                        print("Eliminación cancelada")
                else:
                    print("✗ No se encontró un país con esa temperatura")

            elif opcion == 3:  # Buscar nodo
                print("\n=== BUSCAR NODO ===")
                temperatura = float(input("Temperatura media a buscar: "))

                nodo = arbol.buscar(temperatura)
                if nodo:
                    print(f"✓ País encontrado:")
                    print(f"   ISO3: {nodo.iso3}")
                    print(f"   País: {nodo.pais}")
                    print(f"   Temperatura: {nodo.temperatura_media}°C")

                    realizar_operaciones = input("\n¿Realizar operaciones con este nodo? (s/n): ")
                    if realizar_operaciones.lower() == 's':
                        operaciones_nodo(arbol, nodo)
                else:
                    print("✗ No se encontró un país con esa temperatura")

            elif opcion == 4:  # Buscar nodos con temperatura >= valor
                print("\n=== BUSCAR NODOS CON TEMPERATURA >= VALOR ===")
                temperatura_limite = float(input("Temperatura mínima: "))

                nodos = arbol.buscar_mayor_promedio_global(temperatura_limite)
                if nodos:
                    print(f"\n✓ Se encontraron {len(nodos)} países:")
                    for i, nodo in enumerate(nodos, 1):
                        print(f"   {i}. {nodo.iso3} - {nodo.pais} ({nodo.temperatura_media}°C)")

                    seleccionar = input("\n¿Seleccionar un país para operaciones? (número o 'n'): ")
                    if seleccionar.isdigit():
                        indice = int(seleccionar) - 1
                        if 0 <= indice < len(nodos):
                            operaciones_nodo(arbol, nodos[indice])
                else:
                    print("✗ No se encontraron países con esa temperatura mínima")

            elif opcion == 5:  # Mostrar recorrido por niveles
                print("\n=== RECORRIDO POR NIVELES ===")
                niveles = arbol.recorrido_por_niveles()
                if niveles:
                    for i, nivel in enumerate(niveles):
                        print(f"Nivel {i+1}: {' - '.join(nivel)}")
                else:
                    print("El árbol está vacío")

            elif opcion == 6:  # Mostrar árbol
                arbol.mostrar_arbol_simple()

            elif opcion == 7:  # Operaciones con nodo seleccionado
                print("\n=== SELECCIONAR NODO PARA OPERACIONES ===")
                if not arbol.nodos_almacenados:
                    print("No hay nodos en el árbol")
                else:
                    print("Países disponibles:")
                    for i, nodo in enumerate(arbol.nodos_almacenados, 1):
                        print(f"   {i}. {nodo.iso3} - {nodo.pais} ({nodo.temperatura_media}°C)")

                    try:
                        seleccion = int(input("\nSeleccione un país (número): ")) - 1
                        if 0 <= seleccion < len(arbol.nodos_almacenados):
                            operaciones_nodo(arbol, arbol.nodos_almacenados[seleccion])
                        else:
                            print("Selección inválida")
                    except ValueError:
                        print("Error: Ingrese un número válido")

            elif opcion == 8:  # Salir
                print("\n¡Gracias por usar el programa!")
                break

            else:
                print("Opción inválida")

        except ValueError:
            print("Error: Ingrese un número válido")
        except Exception as e:
            print(f"Error inesperado: {e}")

        if opcion != 8:
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()