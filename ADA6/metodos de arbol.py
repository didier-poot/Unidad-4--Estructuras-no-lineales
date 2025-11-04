from collections import deque
import customtkinter as ctk
import tkinter
class Node:
    """Clase para un nodo individual del árbol."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    """
    Clase para el Árbol Binario de Búsqueda (BST)
    Implementa todos los métodos solicitados.
    """
    def __init__(self):
        # [Constructor]
        self.root = None

    def esVacio(self):
        """Verifica si el árbol está vacío."""
        return self.root is None

    # --- [1] Insertar elemento ---
    def insertar(self, value):
        """Método público para insertar un valor."""
        self.root = self._insertar_recursivo(self.root, value)

    def _insertar_recursivo(self, node, value):
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = self._insertar_recursivo(node.left, value)
        elif value > node.value:
            node.right = self._insertar_recursivo(node.right, value)
        # Si el valor es igual, no hacemos nada (no se permiten duplicados)
        return node

    # --- [4] Buscar un elemento en el árbol ---
    def buscar(self, value):
        """Método público para buscar un valor."""
        return self._buscar_recursivo(self.root, value)

    def _buscar_recursivo(self, node, value):
        if node is None or node.value == value:
            return node is not None
        if value < node.value:
            return self._buscar_recursivo(node.left, value)
        return self._buscar_recursivo(node.right, value)

    # --- Traversals: [5] PreOrden, [6] InOrden, [7] PostOrden ---
    
    def recorrer_preorden(self):
        """Retorna una lista con el recorrido PreOrden."""
        result = []
        self._preorden_recursivo(self.root, result)
        return result

    def _preorden_recursivo(self, node, result):
        if node:
            result.append(node.value)
            self._preorden_recursivo(node.left, result)
            self._preorden_recursivo(node.right, result)

    def recorrer_inorden(self):
        """Retorna una lista con el recorrido InOrden (ordenado)."""
        result = []
        self._inorden_recursivo(self.root, result)
        return result

    def _inorden_recursivo(self, node, result):
        if node:
            self._inorden_recursivo(node.left, result)
            result.append(node.value)
            self._inorden_recursivo(node.right, result)

    def recorrer_postorden(self):
        """Retorna una lista con el recorrido PostOrden."""
        result = []
        self._postorden_recursivo(self.root, result)
        return result

    def _postorden_recursivo(self, node, result):
        if node:
            self._postorden_recursivo(node.left, result)
            self._postorden_recursivo(node.right, result)
            result.append(node.value)

    # --- [10] Recorrer el árbol por niveles (Amplitud) ---
    def recorrer_por_niveles(self):
        """Retorna una lista con el recorrido por niveles (BFS)."""
        if not self.root:
            return []
        
        result = []
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            result.append(node.value)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    # --- [8] Eliminar (PREDECESOR) y [9] Eliminar (SUCESOR) ---
    # Implementaremos el más común (Sucesor) y dejaremos el de Predecesor como ejercicio.
    
    def eliminar(self, value, method='sucesor'):
        """Método público para eliminar un valor."""
        self.root = self._eliminar_recursivo(self.root, value, method)

    def _eliminar_recursivo(self, node, value, method):
        if node is None:
            return node # No se encontró el valor

        # 1. Buscar el nodo a eliminar
        if value < node.value:
            node.left = self._eliminar_recursivo(node.left, value, method)
        elif value > node.value:
            node.right = self._eliminar_recursivo(node.right, value, method)
        else:
            # 2. Nodo encontrado. Casos de eliminación:
            # Caso 1: Nodo hoja (sin hijos)
            if node.left is None and node.right is None:
                return None
            
            # Caso 2: Nodo con un solo hijo
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            
            # Caso 3: Nodo con dos hijos
            if method == 'sucesor':
                # [9] Usando el Sucesor (el menor del subárbol derecho)
                temp_val = self._encontrar_min(node.right)
                node.value = temp_val
                node.right = self._eliminar_recursivo(node.right, temp_val, method)
            else:
                # [8] Usando el Predecesor (el mayor del subárbol izquierdo)
                temp_val = self._encontrar_max(node.left)
                node.value = temp_val
                node.left = self._eliminar_recursivo(node.left, temp_val, method)

        return node

    def _encontrar_min(self, node):
        """Encuentra el valor mínimo en un subárbol (el sucesor)."""
        current = node
        while current.left is not None:
            current = current.left
        return current.value

    def _encontrar_max(self, node):
        """Encuentra el valor máximo en un subárbol (el predecesor)."""
        current = node
        while current.right is not None:
            current = current.right
        return current.value

    # --- [11] Altura del árbol ---
    def altura(self):
        """Retorna la altura del árbol."""
        return self._altura_recursiva(self.root)

    def _altura_recursiva(self, node):
        if node is None:
            return -1 # Un árbol vacío tiene altura -1
        else:
            return 1 + max(self._altura_recursiva(node.left), self._altura_recursiva(node.right))

    # --- [12] Cantidad de hojas del árbol ---
    def cantidad_hojas(self):
        """Retorna el número total de nodos hoja."""
        return self._cantidad_hojas_recursiva(self.root)

    def _cantidad_hojas_recursiva(self, node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1 # Es una hoja
        return self._cantidad_hojas_recursiva(node.left) + self._cantidad_hojas_recursiva(node.right)

    # --- [13] Cantidad de nodos del árbol ---
    def cantidad_nodos(self):
        """Retorna el número total de nodos."""
        return self._cantidad_nodos_recursiva(self.root)

    def _cantidad_nodos_recursiva(self, node):
        if node is None:
            return 0
        return 1 + self._cantidad_nodos_recursiva(node.left) + self._cantidad_nodos_recursiva(node.right)

    # --- [15] Revisa si es un árbol binario completo ---
    def es_binario_completo(self):
        """
        Verifica si el árbol es completo.
        Un árbol completo está lleno en todos sus niveles, excepto posiblemente el último,
        y en el último nivel, todos los nodos están lo más a la izquierda posible.
        """
        if not self.root:
            return True
            
        queue = deque([self.root])
        # Esta bandera se activa cuando encontramos el primer nodo nulo
        encontrado_nulo = False
        
        while queue:
            node = queue.popleft()
            
            if node:
                if encontrado_nulo:
                    # Si ya habíamos visto un nulo, y ahora vemos un nodo, NO es completo
                    return False
                queue.append(node.left)
                queue.append(node.right)
            else:
                # Encontramos el primer nulo
                encontrado_nulo = True
        
        # Si terminamos el recorrido, es completo
        return True

    # --- [16] Revisa si es un árbol binario lleno ---
    def es_binario_lleno(self):
        """
        Verifica si el árbol es lleno.
        Un árbol lleno es aquel donde cada nodo tiene 0 o 2 hijos.
        """
        return self._es_binario_lleno_recursivo(self.root)

    def _es_binario_lleno_recursivo(self, node):
        if node is None:
            return True
        
        # Si es una hoja
        if node.left is None and node.right is None:
            return True
        
        # Si tiene ambos hijos, checamos recursivamente
        if node.left is not None and node.right is not None:
            return self._es_binario_lleno_recursivo(node.left) and self._es_binario_lleno_recursivo(node.right)
        
        # Si solo tiene un hijo, no es lleno
        return False

    # --- [17] Eliminar el árbol ---
    def eliminar_arbol(self):
        """Elimina todos los nodos del árbol."""
        # En Python, simplemente borrando la referencia a la raíz
        # el recolector de basura se encarga del resto.
        self.root = None

    # --- [2] Mostrar árbol completo acostado ---
    def obtener_arbol_acostado(self):
        """
        Retorna un string del árbol "acostado" (raíz a la izquierda).
        Esto es un recorrido InOrden inverso.
        """
        if self.esVacio():
            return "El árbol está vacío."
        
        lineas = []
        self._arbol_acostado_recursivo(self.root, 0, lineas)
        return "\n".join(lineas)

    def _arbol_acostado_recursivo(self, node, nivel, lineas):
        if node is not None:
            # Ir al hijo derecho primero (que se mostrará arriba)
            self._arbol_acostado_recursivo(node.right, nivel + 1, lineas)
            
            # Imprimir el nodo actual
            # Añadimos indentación basada en el nivel
            lineas.append("    " * nivel + "-> " + str(node.value))
            
            # Ir al hijo izquierdo (que se mostrará abajo)
            self._arbol_acostado_recursivo(node.left, nivel + 1, lineas)


#
# PEGAR AQUÍ EL CÓDIGO DE LAS CLASES Node y BinarySearchTree
# (El código completo de la Parte 1)
#
class TreeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Visualizador de Árbol Binario de Búsqueda (Vertical)")
        self.geometry("1000x700")
        
        # Configurar el tema
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Instancia del árbol
        self.tree = BinarySearchTree()
        
        # Constantes de dibujo
        self.RADIO_NODO = 18
        self.ESPACIADO_H = 40  # Espacio horizontal entre nodos
        self.ESPACIADO_V = 60  # Espacio vertical entre niveles
        self.Y_OFFSET = 50     # Margen superior en el canvas

        # Configurar el layout (2 columnas)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- Frame de Controles (Izquierda) ---
        # (Esta sección es idéntica a la anterior, no la repetiré por brevedad)
        # ... solo asegúrate de que todos los 'command' llamen a los
        # métodos correctos (ej. 'command=self.insertar_valor')
        self.control_frame = ctk.CTkFrame(self, width=300)
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.control_label = ctk.CTkLabel(self.control_frame, text="Controles", font=ctk.CTkFont(size=20, weight="bold"))
        self.control_label.pack(pady=12, padx=10)

        # Entrada de valor
        self.entry_valor = ctk.CTkEntry(self.control_frame, placeholder_text="Ingrese un número")
        self.entry_valor.pack(pady=10, padx=10, fill="x")

        # Botones de operación
        self.btn_insertar = ctk.CTkButton(self.control_frame, text="[1] Insertar", command=self.insertar_valor)
        self.btn_insertar.pack(pady=5, padx=10, fill="x")
        
        self.btn_eliminar = ctk.CTkButton(self.control_frame, text="[9] Eliminar (Sucesor)", command=self.eliminar_valor)
        self.btn_eliminar.pack(pady=5, padx=10, fill="x")
        
        self.btn_buscar = ctk.CTkButton(self.control_frame, text="[4] Buscar", command=self.buscar_valor)
        self.btn_buscar.pack(pady=5, padx=10, fill="x")
        
        # Separador
        ctk.CTkLabel(self.control_frame, text="Recorridos y Estadísticas").pack(pady=(15, 5))

        self.btn_inorden = ctk.CTkButton(self.control_frame, text="[6] InOrden", command=self.mostrar_inorden)
        self.btn_inorden.pack(pady=5, padx=10, fill="x")
        
        self.btn_preorden = ctk.CTkButton(self.control_frame, text="[5] PreOrden", command=self.mostrar_preorden)
        self.btn_preorden.pack(pady=5, padx=10, fill="x")
        
        self.btn_postorden = ctk.CTkButton(self.control_frame, text="[7] PostOrden", command=self.mostrar_postorden)
        self.btn_postorden.pack(pady=5, padx=10, fill="x")
        
        self.btn_niveles = ctk.CTkButton(self.control_frame, text="[10] Por Niveles", command=self.mostrar_niveles)
        self.btn_niveles.pack(pady=5, padx=10, fill="x")
        
        self.btn_stats = ctk.CTkButton(self.control_frame, text="[11, 12, 13] Estadísticas", command=self.mostrar_stats)
        self.btn_stats.pack(pady=5, padx=10, fill="x")
        
        self.btn_verificar = ctk.CTkButton(self.control_frame, text="[15, 16] Verificar (Lleno/Completo)", command=self.verificar_propiedades)
        self.btn_verificar.pack(pady=5, padx=10, fill="x")

        self.btn_limpiar = ctk.CTkButton(self.control_frame, text="[17] Eliminar Árbol", command=self.limpiar_arbol, fg_color="red", hover_color="#C00")
        self.btn_limpiar.pack(pady=(15, 5), padx=10, fill="x")


        # --- Frame de Visualización (Derecha) ---
        self.display_frame = ctk.CTkFrame(self)
        self.display_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.display_label = ctk.CTkLabel(self.display_frame, text="[3] Visualización Gráfica del Árbol", font=ctk.CTkFont(size=16, weight="bold"))
        self.display_label.pack(pady=10, padx=10)

        # Canvas para dibujar el árbol
        # Usamos el Canvas de tkinter normal dentro del CTkFrame
        # ya que es más maduro para gráficos.
        self.canvas = tkinter.Canvas(self.display_frame, bg="#2B2B2B", highlightthickness=0)
        self.canvas.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Cuadro de texto para logs y resultados
        self.log_display = ctk.CTkTextbox(self.display_frame, height=100, state="disabled")
        self.log_display.pack(pady=(0, 10), padx=10, fill="x")

        # Actualización inicial
        self.dibujar_arbol()

    # --- Lógica de Dibujo (NUEVO) ---

    def _asignar_coordenadas_inorden(self, node, level, contador_x, posiciones):
        """
        Función recursiva para asignar coordenadas (x_idx, level) a cada nodo.
        Usa un recorrido InOrden para determinar el x_idx.
        'contador_x' es una lista [int] para pasar por referencia.
        'posiciones' es un dict que llenaremos: {valor_nodo: (x_idx, level)}
        """
        if node is None:
            return

        # 1. Recorrer subárbol izquierdo
        self._asignar_coordenadas_inorden(node.left, level + 1, contador_x, posiciones)
        
        # 2. Visitar nodo actual (InOrden)
        # Asignar el índice x actual y el nivel
        posiciones[node.value] = (contador_x[0], level)
        contador_x[0] += 1 # Incrementar el índice x para el próximo nodo
        
        # 3. Recorrer subárbol derecho
        self._asignar_coordenadas_inorden(node.right, level + 1, contador_x, posiciones)

    def _dibujar_nodo_recursivo(self, node, posiciones, x_offset_total):
        """
        Función recursiva para dibujar el árbol en el canvas,
        usando el mapa de 'posiciones' pre-calculado.
        """
        if node is None:
            return

        # 1. Obtener coordenadas del nodo actual
        x_idx, level = posiciones[node.value]
        
        # Calcular coordenadas (x, y) en píxeles
        # Centramos el árbol horizontalmente usando x_offset_total
        x = x_offset_total + (x_idx * self.ESPACIADO_H)
        y = self.Y_OFFSET + (level * self.ESPACIADO_V)

        # 2. Dibujar líneas a los hijos (primero, para que queden detrás)
        if node.left:
            x_hijo_idx, level_hijo = posiciones[node.left.value]
            x_hijo = x_offset_total + (x_hijo_idx * self.ESPACIADO_H)
            y_hijo = self.Y_OFFSET + (level_hijo * self.ESPACIADO_V)
            # Dibuja la línea desde el borde del nodo padre al borde del nodo hijo
            self.canvas.create_line(x, y + self.RADIO_NODO, x_hijo, y_hijo - self.RADIO_NODO, fill="gray", width=1.5)

        if node.right:
            x_hijo_idx, level_hijo = posiciones[node.right.value]
            x_hijo = x_offset_total + (x_hijo_idx * self.ESPACIADO_H)
            y_hijo = self.Y_OFFSET + (level_hijo * self.ESPACIADO_V)
            self.canvas.create_line(x, y + self.RADIO_NODO, x_hijo, y_hijo - self.RADIO_NODO, fill="gray", width=1.5)

        # 3. Dibujar el nodo (círculo y texto)
        self.canvas.create_oval(
            x - self.RADIO_NODO, y - self.RADIO_NODO, 
            x + self.RADIO_NODO, y + self.RADIO_NODO, 
            fill="#333333", outline="#007ACC", width=2
        )
        self.canvas.create_text(x, y, text=str(node.value), fill="white", font=("Arial", 10))

        # 4. Llamadas recursivas para los hijos
        self._dibujar_nodo_recursivo(node.left, posiciones, x_offset_total)
        self._dibujar_nodo_recursivo(node.right, posiciones, x_offset_total)

    def dibujar_arbol(self):
        """Función principal para actualizar el canvas."""
        self.canvas.delete("all") # Limpiar el canvas
        
        if self.tree.esVacio():
            # Usamos winfo_width() para centrar el texto, pero puede ser 0 al inicio
            # así que usamos un valor fijo o esperamos a que se dibuje.
            try:
                width = self.canvas.winfo_width()
            except:
                width = 400 # Valor por defecto
            self.canvas.create_text(width/2, 50, text="El árbol está vacío.", fill="white", font=("Arial", 14))
            return

        # 1. Calcular posiciones
        posiciones = {}
        contador_x = [0] # Usamos lista para pasar por referencia
        self._asignar_coordenadas_inorden(self.tree.root, 0, contador_x, posiciones)
        
        # 2. Calcular el centrado horizontal
        # contador_x[0] ahora tiene el número total de nodos
        ancho_total_arbol = (contador_x[0] - 1) * self.ESPACIADO_H
        try:
            ancho_canvas = self.canvas.winfo_width()
            if ancho_canvas <= 1: ancho_canvas = 500 # Fallback si no está dibujado
        except:
            ancho_canvas = 500 # Fallback
            
        # El offset es para centrar el árbol en el canvas
        x_offset_total = (ancho_canvas - ancho_total_arbol) / 2
        # Asegurarnos de que el offset no sea negativo (si el árbol es muy ancho)
        x_offset_total = max(x_offset_total, self.ESPACIADO_H / 2)

        # 3. Dibujar los nodos
        self._dibujar_nodo_recursivo(self.tree.root, posiciones, x_offset_total)

    # --- Métodos de la GUI (Actualizados para llamar a dibujar_arbol) ---

    def log(self, mensaje):
        """Muestra un mensaje en el cuadro de logs."""
        self.log_display.configure(state="normal")
        self.log_display.delete("1.0", "end")
        self.log_display.insert("1.0", f"Log: {mensaje}")
        self.log_display.configure(state="disabled")

    def _obtener_valor(self):
        """Helper para obtener y validar el valor del entry."""
        try:
            valor = int(self.entry_valor.get())
            self.entry_valor.delete(0, "end")
            return valor
        except ValueError:
            self.log("Error: Ingrese un número entero válido.")
            return None

    def insertar_valor(self):
        valor = self._obtener_valor()
        if valor is not None:
            self.tree.insertar(valor)
            self.dibujar_arbol() # <-- Llamada actualizada
            self.log(f"Valor {valor} insertado.")

    def eliminar_valor(self):
        valor = self._obtener_valor()
        if valor is not None:
            if not self.tree.buscar(valor):
                self.log(f"Error: El valor {valor} no existe en el árbol.")
            else:
                self.tree.eliminar(valor, method='sucesor') # [9]
                self.dibujar_arbol() # <-- Llamada actualizada
                self.log(f"Valor {valor} eliminado (usando sucesor).")

    def buscar_valor(self):
        valor = self._obtener_valor()
        if valor is not None:
            encontrado = self.tree.buscar(valor)
            if encontrado:
                self.log(f"El valor {valor} SÍ se encuentra en el árbol.")
            else:
                self.log(f"El valor {valor} NO se encuentra en el árbol.")

    def mostrar_inorden(self):
        recorrido = self.tree.recorrer_inorden()
        self.log(f"[6] InOrden: {recorrido}")

    def mostrar_preorden(self):
        recorrido = self.tree.recorrer_preorden()
        self.log(f"[5] PreOrden: {recorrido}")

    def mostrar_postorden(self):
        recorrido = self.tree.recorrer_postorden()
        self.log(f"[7] PostOrden: {recorrido}")
        
    def mostrar_niveles(self):
        recorrido = self.tree.recorrer_por_niveles()
        self.log(f"[10] Por Niveles: {recorrido}")

    def mostrar_stats(self):
        altura = self.tree.altura()
        nodos = self.tree.cantidad_nodos()
        hojas = self.tree.cantidad_hojas()
        self.log(f"Estadísticas: \n[11] Altura: {altura} \n[13] Nodos: {nodos} \n[12] Hojas: {hojas}")
        
    def verificar_propiedades(self):
        es_lleno = self.tree.es_binario_lleno()
        es_completo = self.tree.es_binario_completo()
        self.log(f"Propiedades: \n[16] Es Lleno: {es_lleno} \n[15] Es Completo: {es_completo}")

    def limpiar_arbol(self):
        self.tree.eliminar_arbol()
        self.dibujar_arbol() # <-- Llamada actualizada
        self.log("[17] Árbol eliminado.")

app = TreeApp()
app.mainloop()