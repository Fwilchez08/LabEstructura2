
from typing import Optional, List
import graphviz
import csv
import statistics

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
        return f"{self.iso3} ({self.temperatura_media:.2f}°C)"

class LectorDatos:
    """
    En esta clase se leera y procesaran los datos del archivo CSV
    """
    
    @staticmethod
    def cargar_datos_desde_csv(ruta_archivo: str) -> List[tuple]:

        """
        Carga los datos desde el archivo CSV y calcula la media de temperatura
            ruta_archivo: Ruta al archivo CSV
        """
        paises_datos = []
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                
                for fila in lector:
                    # Extraer información básica
                    iso3 = fila['ISO3']
                    pais = fila['Country']
                    
                    # Extraer datos de temperatura de 1961 a 2022
                    temperaturas = []
                    for año in range(1961, 2023):
                        columna = f'F{año}'
                        if columna in fila and fila[columna]:
                            try:
                                temp = float(fila[columna])
                                temperaturas.append(temp)
                            except ValueError:
                                continue
                    
                    # Calcular la media si hay datos disponibles
                    if temperaturas:
                        temperatura_media = statistics.mean(temperaturas)
                        paises_datos.append((iso3, pais, temperatura_media))
                    
            print(f"✓ Se cargaron {len(paises_datos)} países desde el archivo CSV")
            return paises_datos
            
        except FileNotFoundError:
            print(f"✗ Error: No se encontró el archivo {ruta_archivo}")
            return []
        except Exception as e:
            print(f"✗ Error al leer el archivo: {e}")
            return []
    
    @staticmethod
    def cargar_datos_ejemplo() -> List[tuple]:
        """
        Datos de ejemplo para pruebas rápidas
        """
        return [
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

class ArbolAVL:
    """
    Implementación de un árbol AVL
    Utilizando la temperatura media como métrica de comparación
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
        """Función para insertar un nuevo nodo en el árbol"""
        try:
            self.raiz = self._insertar_recursivo(self.raiz, iso3, pais, temperatura_media)
            return True
        except Exception as e:
            print(f"Error al insertar: {e}")
            return False

    def _insertar_recursivo(self, nodo: Optional[Nodo], iso3: str, pais: str, temperatura_media: float) -> Nodo:
        """version recursiva de insertar"""
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
            # Temperaturas iguales, agregar pequeña variación para evitar duplicados
            temperatura_media += 0.001
            nodo.derecho = self._insertar_recursivo(nodo.derecho, iso3, pais, temperatura_media)
            nodo.derecho.padre = nodo

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

    def cargar_datos_masivamente(self, datos: List[tuple]) -> int:
        """
        Carga múltiples países al árbol, devolver cantidad de paises cargados con exito
        usando
            datos: Lista de tuplas (ISO3, País, Temperatura)

        """
        contador = 0
        for iso3, pais, temperatura in datos:
            if self.insertar(iso3, pais, temperatura):
                contador += 1
        return contador

    def buscar(self, temperatura_media: float) -> Optional[Nodo]:
        """Busca un nodo dependiendo de su temperatura media"""
        return self._buscar_recursivo(self.raiz, temperatura_media)

    def _buscar_recursivo(self, nodo: Optional[Nodo], temperatura_media: float) -> Optional[Nodo]:
        """Función recursiva para buscar un nodo"""
        if not nodo or abs(nodo.temperatura_media - temperatura_media) < 0.1:  # Tolerancia mayor para floats
            return nodo

        if temperatura_media < nodo.temperatura_media:
            return self._buscar_recursivo(nodo.izquierdo, temperatura_media)
        else:
            return self._buscar_recursivo(nodo.derecho, temperatura_media)

    def buscar_por_codigo(self, iso3: str) -> Optional[Nodo]:
        """Busca un nodo por su código ISO3"""
        for nodo in self.nodos_almacenados:
            if nodo.iso3.upper() == iso3.upper():
                return nodo
        return None

    def buscar_por_nombre(self, nombre_pais: str) -> List[Nodo]:
        """Busca nodos por nombre de país (búsqueda parcial)"""
        resultados = []
        nombre_lower = nombre_pais.lower()
        for nodo in self.nodos_almacenados:
            if nombre_lower in nodo.pais.lower():
                resultados.append(nodo)
        return resultados

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
        return sorted(resultado, key=lambda x: x.temperatura_media, reverse=True)

    def obtener_estadisticas(self) -> dict:
        """Obtiene estadísticas del dataset"""
        if not self.nodos_almacenados:
            return {}
        
        temperaturas = [nodo.temperatura_media for nodo in self.nodos_almacenados]
        return {
            'total_paises': len(self.nodos_almacenados),
            'temperatura_minima': min(temperaturas),
            'temperatura_maxima': max(temperaturas),
            'temperatura_promedio': statistics.mean(temperaturas),
            'mediana': statistics.median(temperaturas)
        }

    def recorrido_por_niveles(self) -> List[List[str]]:
        """Recorrido por niveles del árbol - Versión recursiva"""
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
            resultado.append(f"{nodo.iso3}({nodo.temperatura_media:.1f}°C)")
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
        
        if abs(nodo_actual.temperatura_media - temperatura_objetivo) < 0.1:
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

    # ===== FUNCIONES DE VISUALIZACIÓN CON GRAPHVIZ =====
    
    def crear_grafico(self, nombre_archivo: str = "arbol_avl", formato: str = "png", 
                     mostrar_detalles: bool = True, resaltar_nodo: Optional[Nodo] = None) -> bool:
        """
        Crea una visualización gráfica del árbol AVL usando Graphviz
        
        Args:
            nombre_archivo: Nombre del archivo de salida
            formato: Formato de salida ('png', 'pdf', 'svg', etc.)
            mostrar_detalles: Si mostrar información adicional en los nodos
            resaltar_nodo: Nodo específico para resaltar en el gráfico
        
        Returns:
            bool: True si se creó exitosamente, False en caso contrario
        """
        if not self.raiz:
            print("El árbol está vacío, no se puede crear el gráfico")
            return False
        
        try:
            # Crear objeto Digraph
            dot = graphviz.Digraph(comment='Árbol AVL - Temperaturas por País')
            
            # Configuración del gráfico
            dot.attr(rankdir='TB')  # Top to Bottom
            dot.attr('node', 
                    shape='circle', 
                    style='filled',
                    fontname='Arial',
                    fontsize='10')
            dot.attr('edge', 
                    fontname='Arial',
                    fontsize='8')
            
            # Agregar título
            estadisticas = self.obtener_estadisticas()
            dot.attr(label=f'\\nÁrbol AVL - Temperaturas por País\\n' + 
                          f'Total: {estadisticas.get("total_paises", 0)} países | ' +
                          f'Rango: {estadisticas.get("temperatura_minima", 0):.1f}°C - {estadisticas.get("temperatura_maxima", 0):.1f}°C',
                    fontsize='14',
                    fontname='Arial Bold')
            
            # Agregar nodos y aristas
            self._agregar_nodos_graphviz(dot, self.raiz, mostrar_detalles, resaltar_nodo)
            
            # Renderizar el gráfico
            dot.render(nombre_archivo, format=formato, cleanup=True)
            print(f"✓ Gráfico creado exitosamente: {nombre_archivo}.{formato}")
            return True
            
        except Exception as e:
            print(f"Error al crear el gráfico: {e}")
            print("Asegúrese de tener Graphviz instalado en su sistema")
            return False

    def _agregar_nodos_graphviz(self, dot, nodo: Optional[Nodo], mostrar_detalles: bool, resaltar_nodo: Optional[Nodo]):
        """Función recursiva para agregar nodos al gráfico de Graphviz"""
        if not nodo:
            return
        
        # Crear ID único para el nodo
        node_id = f"nodo_{id(nodo)}"
        
        # Determinar color del nodo
        if resaltar_nodo and nodo == resaltar_nodo:
            color = 'gold'
            penwidth = '3'
        else:
            # Color basado en la temperatura
            temp = nodo.temperatura_media
            if temp < 0:
                color = 'lightcyan'
            elif temp < 10:
                color = 'lightblue'
            elif temp < 20:
                color = 'lightgreen'
            elif temp < 30:
                color = 'orange'
            else:
                color = 'salmon'
            penwidth = '1'
        
        # Crear etiqueta del nodo
        if mostrar_detalles:
            factor_balance = self.obtener_factor_balance(nodo)
            etiqueta = f"{nodo.iso3}\\n{nodo.temperatura_media:.1f}°C\\n" + \
                      f"Alt: {nodo.altura} | FB: {factor_balance}"
        else:
            etiqueta = f"{nodo.iso3}\\n{nodo.temperatura_media:.1f}°C"
        
        # Agregar nodo al gráfico
        dot.node(node_id, 
                label=etiqueta,
                fillcolor=color,
                penwidth=penwidth)
        
        # Agregar aristas a los hijos
        if nodo.izquierdo:
            child_id = f"nodo_{id(nodo.izquierdo)}"
            dot.edge(node_id, child_id, label='I', color='blue')
            self._agregar_nodos_graphviz(dot, nodo.izquierdo, mostrar_detalles, resaltar_nodo)
        
        if nodo.derecho:
            child_id = f"nodo_{id(nodo.derecho)}"
            dot.edge(node_id, child_id, label='D', color='red')
            self._agregar_nodos_graphviz(dot, nodo.derecho, mostrar_detalles, resaltar_nodo)

    def crear_grafico_con_leyenda(self, nombre_archivo: str = "arbol_avl_detallado", 
                                 formato: str = "png") -> bool:
        """
        Crea un gráfico del árbol con leyenda explicativa
        """
        if not self.raiz:
            print("El árbol está vacío, no se puede crear el gráfico")
            return False
        
        try:
            # Crear objeto Digraph principal
            dot = graphviz.Digraph(comment='Árbol AVL con Leyenda')
            dot.attr(compound='true')
            
            # Subgráfico para el árbol
            with dot.subgraph(name='cluster_arbol') as arbol:
                arbol.attr(label='Árbol AVL - Dataset de Temperaturas', fontsize='14', fontname='Arial Bold')
                arbol.attr(style='filled', color='lightgrey')
                
                # Configuración del árbol
                arbol.attr('node', 
                          shape='circle', 
                          style='filled',
                          fontname='Arial',
                          fontsize='10')
                arbol.attr('edge', 
                          fontname='Arial',
                          fontsize='8')
                
                # Agregar nodos del árbol
                self._agregar_nodos_graphviz(arbol, self.raiz, True, None)
            
            # Subgráfico para la leyenda
            with dot.subgraph(name='cluster_leyenda') as leyenda:
                leyenda.attr(label='Leyenda de Colores', fontsize='14', fontname='Arial Bold')
                leyenda.attr(style='filled', color='white')
                
                # Nodos de leyenda
                leyenda.node('l0', '< 0°C', fillcolor='lightcyan', style='filled')
                leyenda.node('l1', '0-10°C', fillcolor='lightblue', style='filled')
                leyenda.node('l2', '10-20°C', fillcolor='lightgreen', style='filled')
                leyenda.node('l3', '20-30°C', fillcolor='orange', style='filled')
                leyenda.node('l4', '> 30°C', fillcolor='salmon', style='filled')
                
                # Organizar leyenda verticalmente
                leyenda.edge('l0', 'l1', style='invisible')
                leyenda.edge('l1', 'l2', style='invisible')
                leyenda.edge('l2', 'l3', style='invisible')
                leyenda.edge('l3', 'l4', style='invisible')
            
            # Renderizar
            dot.render(nombre_archivo, format=formato, cleanup=True)
            print(f"✓ Gráfico detallado creado: {nombre_archivo}.{formato}")
            return True
            
        except Exception as e:
            print(f"Error al crear el gráfico detallado: {e}")
            return False

    def visualizar_busqueda(self, temperatura_objetivo: float, nombre_archivo: str = "busqueda_avl") -> bool:
        """
        Crea una visualización del camino de búsqueda para una temperatura específica
        """
        nodo_encontrado = self.buscar(temperatura_objetivo)
        
        try:
            dot = graphviz.Digraph(comment='Visualización de Búsqueda AVL')
            dot.attr(rankdir='TB')
            dot.attr('node', shape='circle', style='filled', fontname='Arial', fontsize='10')
            dot.attr('edge', fontname='Arial', fontsize='8')
            
            # Agregar título
            if nodo_encontrado:
                titulo = f'Búsqueda exitosa: {temperatura_objetivo}°C\\nEncontrado: {nodo_encontrado.iso3} ({nodo_encontrado.temperatura_media:.1f}°C)'
            else:
                titulo = f'Búsqueda fallida: {temperatura_objetivo}°C\\nNo encontrado'
            
            dot.attr(label='\\n' + titulo, fontsize='14', fontname='Arial Bold')
            
            # Crear conjunto de nodos en el camino de búsqueda
            camino_busqueda = set()
            self._marcar_camino_busqueda(self.raiz, temperatura_objetivo, camino_busqueda)
            
            # Agregar nodos con colores especiales para el camino
            self._agregar_nodos_busqueda(dot, self.raiz, camino_busqueda, nodo_encontrado)
            
            dot.render(nombre_archivo, format='png', cleanup=True)
            print(f"✓ Visualización de búsqueda creada: {nombre_archivo}.png")
            return True
            
        except Exception as e:
            print(f"Error al crear la visualización de búsqueda: {e}")
            return False

    def _marcar_camino_busqueda(self, nodo: Optional[Nodo], temperatura_objetivo: float, camino: set):
        """Marca los nodos que forman parte del camino de búsqueda"""
        if not nodo:
            return False
        
        # Agregar nodo actual al camino
        camino.add(nodo)
        
        # Si encontramos el objetivo, retornar True
        if abs(nodo.temperatura_media - temperatura_objetivo) < 0.1:
            return True
        
        # Continuar búsqueda
        if temperatura_objetivo < nodo.temperatura_media:
            if self._marcar_camino_busqueda(nodo.izquierdo, temperatura_objetivo, camino):
                return True
        else:
            if self._marcar_camino_busqueda(nodo.derecho, temperatura_objetivo, camino):
                return True
        
        # Si llegamos aquí, este nodo no está en el camino exitoso
        camino.discard(nodo)
        return False

    def _agregar_nodos_busqueda(self, dot, nodo: Optional[Nodo], camino_busqueda: set, nodo_objetivo: Optional[Nodo]):
        """Agregar nodos con colores especiales para visualizar la búsqueda"""
        if not nodo:
            return
        
        node_id = f"nodo_{id(nodo)}"
        
        # Determinar color del nodo
        if nodo == nodo_objetivo:
            color = 'gold'
            penwidth = '3'
        elif nodo in camino_busqueda:
            color = 'lightcoral'
            penwidth = '2'
        else:
            color = 'lightgray'
            penwidth = '1'
        
        # Etiqueta del nodo
        etiqueta = f"{nodo.iso3}\\n{nodo.temperatura_media:.1f}°C"
        
        dot.node(node_id, 
                label=etiqueta,
                fillcolor=color,
                penwidth=penwidth)
        
        # Agregar aristas
        if nodo.izquierdo:
            child_id = f"nodo_{id(nodo.izquierdo)}"
            edge_color = 'red' if nodo.izquierdo in camino_busqueda else 'gray'
            dot.edge(node_id, child_id, label='I', color=edge_color)
            self._agregar_nodos_busqueda(dot, nodo.izquierdo, camino_busqueda, nodo_objetivo)
        
        if nodo.derecho:
            child_id = f"nodo_{id(nodo.derecho)}"
            edge_color = 'red' if nodo.derecho in camino_busqueda else 'gray'
            dot.edge(node_id, child_id, label='D', color=edge_color)
            self._agregar_nodos_busqueda(dot, nodo.derecho, camino_busqueda, nodo_objetivo)

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
        
        print(f"{prefijo}{'└── ' if es_ultimo else '├── '}{nodo.iso3} ({nodo.temperatura_media:.1f}°C)")
        
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
    print("\n" + "="*70)
    print("    LABORATORIO AVL - ESTRUCTURA DE DATOS II")
    print("="*70)
    print("1.  Insertar nodo manualmente")
    print("2.  Eliminar nodo")
    print("3.  Buscar nodo por temperatura")
    print("4.  Buscar nodo por código ISO3")
    print("5.  Buscar nodo por nombre de país")
    print("6.  Buscar países con temperatura >= valor")
    print("7.  Mostrar recorrido por niveles")
    print("8.  Mostrar estadísticas del dataset")
    print("9. Operaciones con nodo seleccionado")
    print("-" * 70)
    print("10.  Crear gráfico simple del árbol")
    print("11. crear gráfico detallado con leyenda")
    print("12.  Visualizar búsqueda de un nodo")
    print("13.  Resaltar nodo específico en gráfico")
    print("14.  Recargar datos desde CSV")
    print("-" * 70)
    print("15. Salir")
    print("="*70)

def operaciones_nodo(arbol: ArbolAVL, nodo: Nodo):
    """Submenú para operaciones específicas con un nodo"""
    while True:
        print(f"\n=== OPERACIONES CON NODO: {nodo.iso3} ===")
        print(f"País: {nodo.pais}")
        print(f"Temperatura media: {nodo.temperatura_media:.2f}°C")
        print("\n1. Obtener nivel del nodo")
        print("2. Obtener factor de balanceo")
        print("3. Encontrar padre")
        print("4. Encontrar abuelo")
        print("5. Encontrar tío")
        print("6. Crear gráfico resaltando este nodo")
        print("7. Volver al menú principal")
        
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
                    print(f"Padre de {nodo.iso3}: {padre.iso3} ({padre.temperatura_media:.1f}°C)")
                else:
                    print(f"El nodo {nodo.iso3} es la raíz (no tiene padre)")
                    
            elif opcion == 4:
                abuelo = arbol.obtener_abuelo(nodo)
                if abuelo:
                    print(f"Abuelo de {nodo.iso3}: {abuelo.iso3} ({abuelo.temperatura_media:.1f}°C)")
                else:
                    print(f"El nodo {nodo.iso3} no tiene abuelo")
                    
            elif opcion == 5:
                tio = arbol.obtener_tio(nodo)
                if tio:
                    print(f"Tío de {nodo.iso3}: {tio.iso3} ({tio.temperatura_media:.1f}°C)")
                else:
                    print(f"El nodo {nodo.iso3} no tiene tío")
                    
            elif opcion == 6:
                nombre_archivo = f"nodo_{nodo.iso3}_resaltado"
                arbol.crear_grafico(nombre_archivo, "png", True, nodo)
                
            elif opcion == 7:
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
    
    print("¡Bienvenido al Laboratorio de Árbol AVL con Visualización Gráfica!")
    print("="*70)
    
    # Intentar cargar datos desde CSV
    ruta_csv = input("Ingrese la ruta del archivo CSV (o Enter para datos de prueba): ").strip()
    if not ruta_csv:
        ruta_csv = "datos de prueba"
    
    datos_csv = LectorDatos.cargar_datos_desde_csv(ruta_csv)
    
    if datos_csv:
        print(f"\n¿Cargar todos los {len(datos_csv)} países del CSV? (s/n): ", end="")
        if input().lower() == 's':
            print("\nCargando datos del CSV...")
            cargados = arbol.cargar_datos_masivamente(datos_csv)
            print(f"✓ Se cargaron {cargados} países exitosamente")
            
            # Mostrar estadísticas
            stats = arbol.obtener_estadisticas()
            print(f"\nESTADÍSTICAS DEL DATASET:")
            print(f"   Total países: {stats['total_paises']}")
            print(f"   Temperatura mínima: {stats['temperatura_minima']:.2f}°C")
            print(f"   Temperatura máxima: {stats['temperatura_maxima']:.2f}°C")
            print(f"   Temperatura promedio: {stats['temperatura_promedio']:.2f}°C")
            print(f"   Mediana: {stats['mediana']:.2f}°C")
            
            # Crear gráfico inicial
            print("\n¿Crear gráfico inicial del árbol? (s/n): ", end="")
            if input().lower() == 's':
                arbol.crear_grafico("arbol_inicial_csv")
        else:
            print("Datos del CSV disponibles pero no cargados")
    else:
        print("\n  No se pudieron cargar datos del CSV")
        print("¿Cargar datos de ejemplo? (s/n): ", end="")
        if input().lower() == 's':
            datos_ejemplo = LectorDatos.cargar_datos_ejemplo()
            cargados = arbol.cargar_datos_masivamente(datos_ejemplo)
            print(f"Se cargaron {cargados} países de ejemplo")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = int(input("Seleccione una opción: "))
            
            if opcion == 1:  # Insertar nodo manualmente
                print("\n=== INSERTAR NODO MANUALMENTE ===")
                iso3 = input("Código ISO3 del país: ").upper()
                pais = input("Nombre del país: ")
                temperatura = float(input("Temperatura media (°C): "))
                
                if arbol.insertar(iso3, pais, temperatura):
                    print(f"✓ País {iso3} insertado correctamente")
                    print("\n¿Crear gráfico actualizado? (s/n): ", end="")
                    if input().lower() == 's':
                        arbol.crear_grafico("arbol_despues_insercion")
                else:
                    print("✗ Error al insertar el país")
                    
            elif opcion == 2:  # Eliminar nodo
                print("\n=== ELIMINAR NODO ===")
                temperatura = float(input("Temperatura media del país a eliminar: "))
                
                nodo = arbol.buscar(temperatura)
                if nodo:
                    print(f"País encontrado: {nodo.iso3} - {nodo.pais} ({nodo.temperatura_media:.2f}°C)")
                    confirmar = input("¿Confirma la eliminación? (s/n): ")
                    if confirmar.lower() == 's':
                        if arbol.eliminar(temperatura):
                            print("✓ País eliminado correctamente")
                            print("\n¿Crear gráfico actualizado? (s/n): ", end="")
                            if input().lower() == 's':
                                arbol.crear_grafico("arbol_despues_eliminacion")
                        else:
                            print("✗ Error al eliminar el país")
                    else:
                        print("Eliminación cancelada")
                else:
                    print("✗ No se encontró un país con esa temperatura")
                    
            elif opcion == 3:  # Buscar por temperatura
                print("\n=== BUSCAR NODO POR TEMPERATURA ===")
                temperatura = float(input("Temperatura media a buscar: "))
                
                nodo = arbol.buscar(temperatura)
                if nodo:
                    print(f"✓ País encontrado:")
                    print(f"   ISO3: {nodo.iso3}")
                    print(f"   País: {nodo.pais}")
                    print(f"   Temperatura: {nodo.temperatura_media:.2f}°C")
                    
                    print("\n¿Qué desea hacer?")
                    print("1. Visualizar búsqueda")
                    print("2. Operaciones con este nodo")
                    print("3. Continuar")
                    
                    sub_opcion = input("Seleccione (1/2/3): ")
                    if sub_opcion == '1':
                        arbol.visualizar_busqueda(temperatura)
                    elif sub_opcion == '2':
                        operaciones_nodo(arbol, nodo)
                else:
                    print("✗ No se encontró un país con esa temperatura")
                    print("\n¿Visualizar búsqueda fallida? (s/n): ", end="")
                    if input().lower() == 's':
                        arbol.visualizar_busqueda(temperatura)

            elif opcion == 4:  # Buscar por código ISO3
                print("\n=== BUSCAR NODO POR CÓDIGO ISO3 ===")
                iso3 = input("Código ISO3 a buscar: ").upper()
                
                nodo = arbol.buscar_por_codigo(iso3)
                if nodo:
                    print(f"✓ País encontrado:")
                    print(f"   ISO3: {nodo.iso3}")
                    print(f"   País: {nodo.pais}")
                    print(f"   Temperatura: {nodo.temperatura_media:.2f}°C")
                    
                    realizar_operaciones = input("\n¿Realizar operaciones con este nodo? (s/n): ")
                    if realizar_operaciones.lower() == 's':
                        operaciones_nodo(arbol, nodo)
                else:
                    print(f"✗ No se encontró un país con código {iso3}")

            elif opcion == 5:  # Buscar por nombre
                print("\n=== BUSCAR NODO POR NOMBRE DE PAÍS ===")
                nombre = input("Nombre del país (búsqueda parcial): ")
                
                nodos = arbol.buscar_por_nombre(nombre)
                if nodos:
                    print(f"✓ Se encontraron {len(nodos)} países:")
                    for i, nodo in enumerate(nodos, 1):
                        print(f"   {i}. {nodo.iso3} - {nodo.pais} ({nodo.temperatura_media:.2f}°C)")
                    
                    if len(nodos) == 1:
                        realizar_operaciones = input("\n¿Realizar operaciones con este nodo? (s/n): ")
                        if realizar_operaciones.lower() == 's':
                            operaciones_nodo(arbol, nodos[0])
                    else:
                        seleccionar = input("\n¿Seleccionar un país para operaciones? (número o 'n'): ")
                        if seleccionar.isdigit():
                            indice = int(seleccionar) - 1
                            if 0 <= indice < len(nodos):
                                operaciones_nodo(arbol, nodos[indice])
                else:
                    print(f"✗ No se encontraron países que contengan '{nombre}'")
                    
            elif opcion == 6:  # Buscar países con temperatura >= valor
                print("\n=== BUSCAR PAÍSES CON TEMPERATURA >= VALOR ===")
                temperatura_limite = float(input("Temperatura mínima: "))
                
                nodos = arbol.buscar_mayor_promedio_global(temperatura_limite)
                if nodos:
                    print(f"\n✓ Se encontraron {len(nodos)} países:")
                    for i, nodo in enumerate(nodos[:10], 1):  # Mostrar solo los primeros 10
                        print(f"   {i}. {nodo.iso3} - {nodo.pais} ({nodo.temperatura_media:.2f}°C)")
                    
                    if len(nodos) > 10:
                        print(f"   ... y {len(nodos) - 10} más")
                    
                    seleccionar = input("\n¿Seleccionar un país para operaciones? (número o 'n'): ")
                    if seleccionar.isdigit():
                        indice = int(seleccionar) - 1
                        if 0 <= indice < min(10, len(nodos)):
                            operaciones_nodo(arbol, nodos[indice])
                else:
                    print("✗ No se encontraron países con esa temperatura mínima")
                    
            elif opcion == 7:  # Recorrido por niveles
                print("\n=== RECORRIDO POR NIVELES ===")
                niveles = arbol.recorrido_por_niveles()
                if niveles:
                    for i, nivel in enumerate(niveles):
                        print(f"Nivel {i+1}: {' | '.join(nivel)}")
                else:
                    print("El árbol está vacío")
            
                
            elif opcion == 8:  # Estadísticas
                print("\n=== ESTADÍSTICAS DEL DATASET ===")
                stats = arbol.obtener_estadisticas()
                if stats:
                    print(f" Total de países: {stats['total_paises']}")
                    print(f"  Temperatura mínima: {stats['temperatura_minima']:.2f}°C")
                    print(f"  Temperatura máxima: {stats['temperatura_maxima']:.2f}°C")
                    print(f" Temperatura promedio: {stats['temperatura_promedio']:.2f}°C")
                    print(f" Mediana: {stats['mediana']:.2f}°C")
                else:
                    print("No hay datos en el árbol")
                    
            elif opcion == 9:  # Operaciones con nodo seleccionado
                print("\n=== SELECCIONAR NODO PARA OPERACIONES ===")
                if not arbol.nodos_almacenados:
                    print("No hay nodos en el árbol")
                else:
                    # Mostrar países ordenados por temperatura
                    paises_ordenados = sorted(arbol.nodos_almacenados, key=lambda x: x.temperatura_media)
                    print("Países disponibles (ordenados por temperatura):")
                    
                    for i, nodo in enumerate(paises_ordenados[:15], 1):  # Mostrar primeros 15
                        print(f"   {i}. {nodo.iso3} - {nodo.pais} ({nodo.temperatura_media:.1f}°C)")
                    
                    if len(paises_ordenados) > 15:
                        print(f"   ... y {len(paises_ordenados) - 15} más")
                    
                    try:
                        seleccion = int(input("\nSeleccione un país (número): ")) - 1
                        if 0 <= seleccion < min(15, len(paises_ordenados)):
                            operaciones_nodo(arbol, paises_ordenados[seleccion])
                        else:
                            print("Selección inválida")
                    except ValueError:
                        print("Error: Ingrese un número válido")
                        
            elif opcion == 10:  # Gráfico simple
                arbol.crear_grafico()
                
            elif opcion == 11:  # Gráfico detallado
                arbol.crear_grafico_con_leyenda()
                
            elif opcion == 12:  # Visualizar búsqueda
                print("\n=== VISUALIZAR BÚSQUEDA ===")
                try:
                    temp = float(input("Temperatura a buscar: "))
                    arbol.visualizar_busqueda(temp)
                except ValueError:
                    print("Error: Ingrese una temperatura válida")
                    
            elif opcion == 13:  # Resaltar nodo específico
                print("\n=== RESALTAR NODO ===")
                try:
                    codigo = input("Código ISO3 del país a resaltar: ").upper()
                    nodo = arbol.buscar_por_codigo(codigo)
                    if nodo:
                        nombre = input("Nombre del archivo (Enter para 'arbol_resaltado'): ") or "arbol_resaltado"
                        arbol.crear_grafico(nombre, "png", True, nodo)
                        print(f"País {nodo.pais} resaltado en el gráfico")
                    else:
                        print(f"No se encontró un país con código {codigo}")
                except Exception as e:
                    print(f"Error: {e}")

            elif opcion == 14:  # Recargar datos
                print("\n=== RECARGAR DATOS DESDE CSV ===")
                ruta_csv = input("Ingrese la ruta del archivo CSV: ").strip()
                if ruta_csv:
                    datos_nuevos = LectorDatos.cargar_datos_desde_csv(ruta_csv)
                    if datos_nuevos:
                        confirmar = input(f"¿Reemplazar árbol actual con {len(datos_nuevos)} nuevos países? (s/n): ")
                        if confirmar.lower() == 's':
                            # Limpiar árbol actual
                            arbol = ArbolAVL()
                            cargados = arbol.cargar_datos_masivamente(datos_nuevos)
                            print(f"✓ Árbol recargado con {cargados} países")
                            
                            # Mostrar nuevas estadísticas
                            stats = arbol.obtener_estadisticas()
                            print(f"Nuevas estadísticas:")
                            print(f"   Rango: {stats['temperatura_minima']:.1f}°C - {stats['temperatura_maxima']:.1f}°C")
                            print(f"   Promedio: {stats['temperatura_promedio']:.1f}°C")
                    
            elif opcion == 15:  # Salir
                print("\n¡Gracias por usar el programa!")
                break
                
            else:
                print("Opción inválida")
                
        except ValueError:
            print("Error: Por favor ingrese un número válido")
        except Exception as e:
            print(f"Error inesperado: {e}")
            
        if opcion != 16:
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    # Verificación si Graphviz está disponible
    try:
        import graphviz
        print("Graphviz disponible")
    except ImportError:
        print(" Graphviz no está instalado")

    main()
