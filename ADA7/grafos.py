import customtkinter as ctk
import math
import random
import os # <-- ¡NUEVO!

# --- ¡NUEVO! ---
# Importar la librería de imágenes de Pillow
try:
    from PIL import Image, ImageTk
except ImportError:
    print("Error: Se necesita la librería Pillow. Instálala con: pip install Pillow")
    exit()

# --- 1. CLASES DE LA ESTRUCTURA DE DATOS ---
# (Tu clase Graph, Vertex y Edge va aquí - sin cambios)
class Graph:
    """Clase principal del Grafo."""

    class Vertex:
        """Clase interna para representar un Vértice."""
        def __init__(self, element, uid):
            self._element = element
            self._uid = uid  # ID único (ej: "v1", "v2")
            self._incoming = {}  # {edge_uid: Edge}
            self._outgoing = {}  # {edge_uid: Edge}

        def __str__(self):
            return str(self._element)

    class Edge:
        """Clase interna para representar una Arista."""
        def __init__(self, element, uid, origin, destination, directed=False):
            self._element = element
            self._uid = uid  # ID único (ej: "e1", "e2")
            self._origin = origin
            self._destination = destination
            self._directed = directed

        def __str__(self):
            return str(self._element)

        def endpoints(self):
            """Devuelve la tupla de vértices finales."""
            return (self._origin, self._destination)

        def opposite(self, v):
            """Devuelve el vértice opuesto a v en esta arista."""
            if not isinstance(v, Graph.Vertex):
                raise TypeError("v debe ser una instancia de Vertex")
            if self._origin == v:
                return self._destination
            elif self._destination == v:
                return self._origin
            else:
                raise ValueError("v no es un vértice incidente de esta arista")

    def __init__(self):
        """Crea un grafo vacío."""
        self._vertices = {}  # {vertex_uid: Vertex}
        self._edges = {}     # {edge_uid: Edge}
        self._v_counter = 0  # Para IDs únicos de vértices
        self._e_counter = 0  # Para IDs únicos de aristas

    def _validate_vertex(self, v_uid):
        """Valida si el UID del vértice existe y devuelve el objeto Vertex."""
        if v_uid not in self._vertices:
            raise ValueError(f"Vértice '{v_uid}' no existe en el grafo.")
        return self._vertices[v_uid]

    def _validate_edge(self, e_uid):
        """Valida si el UID de la arista existe y devuelve el objeto Edge."""
        if e_uid not in self._edges:
            raise ValueError(f"Arista '{e_uid}' no existe en el grafo.")
        return self._edges[e_uid]

    # --- Operaciones Generales ---

    def numVertices(self):
        """Devuelve el número de vértices de G."""
        return len(self._vertices)

    def numAristas(self):
        """Devuelve el número de aristas de G."""
        return len(self._edges)

    def vertices(self):
        """Devuelve una lista de los UIDs de los vértices de G."""
        return list(self._vertices.keys())
    
    def get_vertex_element(self, v_uid):
        """Devuelve el elemento (dato) de un vértice dado su UID."""
        v = self._validate_vertex(v_uid)
        return v._element

    def aristas(self):
        """Devuelve una lista de los UIDs de las aristas de G."""
        return list(self._edges.keys())

    def grado(self, v_uid):
        """Devuelve el grado de v."""
        v = self._validate_vertex(v_uid)
        # Combina aristas de entrada y salida (para contar no dirigidas una vez)
        incident_edges = {**v._incoming, **v._outgoing}
        return len(incident_edges)

    def verticesAdyacentes(self, v_uid):
        """Devuelve una lista de los UIDs de los vértices adyacentes a v."""
        v = self._validate_vertex(v_uid)
        adyacentes = set()
        incident_edges = {**v._incoming, **v._outgoing}
        for edge in incident_edges.values():
            adyacentes.add(edge.opposite(v)._uid)
        return list(adyacentes)

    def aristasIncidentes(self, v_uid):
        """Devuelve una lista de los UIDs de las aristas incidentes en v."""
        v = self._validate_vertex(v_uid)
        incident_edges = {**v._incoming, **v._outgoing}
        return list(incident_edges.keys())

    def verticesFinales(self, e_uid):
        """Devuelve un array (tupla) con los UIDs de los vértices finales de e."""
        e = self._validate_edge(e_uid)
        v1, v2 = e.endpoints()
        return (v1._uid, v2._uid)

    def opuesto(self, v_uid, e_uid):
        """Devuelve el UID del punto extremo de la arista e diferente a v."""
        v = self._validate_vertex(v_uid)
        e = self._validate_edge(e_uid)
        opuesto_v = e.opposite(v)
        return opuesto_v._uid

    def esAdyacente(self, v_uid, w_uid):
        """Devuelve verdadero si los vértices v y w son adyacentes."""
        # Simple: w está en la lista de adyacentes de v.
        return w_uid in self.verticesAdyacentes(v_uid)

    # --- Operaciones con aristas dirigidas ---

    def aristasDirigidas(self):
        """Devuelve una lista de todas las aristas dirigidas."""
        return [uid for uid, e in self._edges.items() if e._directed]

    def aristasNodirigidas(self):
        """Devuelve una lista de todas las aristas no dirigidas."""
        return [uid for uid, e in self._edges.items() if not e._directed]

    def gradoEnt(self, v_uid):
        """Devuelve el grado de entrada de v."""
        v = self._validate_vertex(v_uid)
        return len(v._incoming)

    def gradoSalida(self, v_uid):
        """Devuelve el grado de salida de v."""
        v = self._validate_vertex(v_uid)
        return len(v._outgoing)

    def aristasIncidentesEnt(self, v_uid):
        """Devuelve una lista de todas las aristas de entrada a v."""
        v = self._validate_vertex(v_uid)
        return list(v._incoming.keys())

    def aristasIncidentesSal(self, v_uid):
        """Devuelve una lista de todas las aristas de salida a v."""
        v = self._validate_vertex(v_uid)
        return list(v._outgoing.keys())

    def verticesAdyacentesEnt(self, v_uid):
        """Devuelve lista de vértices adyacentes a v a través de aristas de entrada."""
        v = self._validate_vertex(v_uid)
        adyacentes = set()
        for edge in v._incoming.values():
            if edge._directed:
                adyacentes.add(edge._origin._uid)
            else:
                adyacentes.add(edge.opposite(v)._uid)
        return list(adyacentes)

    def verticesAdyacentesSal(self, v_uid):
        """Devuelve lista de vértices adyacentes a v a través de aristas de salida."""
        v = self._validate_vertex(v_uid)
        adyacentes = set()
        for edge in v._outgoing.values():
            if edge._directed:
                adyacentes.add(edge._destination._uid)
            else:
                adyacentes.add(edge.opposite(v)._uid)
        return list(adyacentes)

    def destino(self, e_uid):
        """Devuelve el destino de la arista dirigida e."""
        e = self._validate_edge(e_uid)
        if not e._directed:
            raise ValueError("La arista no es dirigida")
        return e._destination._uid

    def origen(self, e_uid):
        """Devuelve el origen de la arista dirigida e."""
        e = self._validate_edge(e_uid)
        if not e._directed:
            raise ValueError("La arista no es dirigida")
        return e._origin._uid

    def esDirigida(self, e_uid):
        """Devuelve verdadero si la arista e es dirigida."""
        e = self._validate_edge(e_uid)
        return e._directed

    # --- Operaciones para actualizar grafos ---

    def insertaVertice(self, o):
        """Inserta y devuelve un nuevo vértice (su UID) almacenando el objeto o."""
        v_uid = f"v{self._v_counter}"
        self._v_counter += 1
        nuevo_v = self.Vertex(o, v_uid)
        self._vertices[v_uid] = nuevo_v
        return v_uid

    def insertaArista(self, v_uid, w_uid, o):
        """Inserta y devuelve una arista no dirigida (su UID) entre v y w."""
        v = self._validate_vertex(v_uid)
        w = self._validate_vertex(w_uid)
        
        e_uid = f"e{self._e_counter}"
        self._e_counter += 1
        
        nueva_e = self.Edge(o, e_uid, v, w, directed=False)
        self._edges[e_uid] = nueva_e
        
        # Al ser no dirigida, es entrante y saliente para ambos
        v._incoming[e_uid] = nueva_e
        v._outgoing[e_uid] = nueva_e
        w._incoming[e_uid] = nueva_e
        w._outgoing[e_uid] = nueva_e
        
        return e_uid

    def insertaAristaDirigida(self, v_uid, w_uid, o):
        """Inserta y devuelve una arista dirigida (su UID) de v a w."""
        v = self._validate_vertex(v_uid)
        w = self._validate_vertex(w_uid)
        
        e_uid = f"e{self._e_counter}"
        self._e_counter += 1
        
        nueva_e = self.Edge(o, e_uid, v, w, directed=True)
        self._edges[e_uid] = nueva_e
        
        # Al ser dirigida, es saliente de v y entrante a w
        v._outgoing[e_uid] = nueva_e
        w._incoming[e_uid] = nueva_e
        
        return e_uid

    def eliminaVertice(self, v_uid):
        """Elimina vértice v y todas las aristas incidentes."""
        v = self._validate_vertex(v_uid)
        
        # Eliminar todas las aristas incidentes (copiamos keys para evitar error de tamaño)
        aristas_a_eliminar = list(self.aristasIncidentes(v_uid))
        for e_uid in aristas_a_eliminar:
            self.eliminaArista(e_uid)
            
        # Eliminar el vértice
        del self._vertices[v_uid]

    def eliminaArista(self, e_uid):
        """Elimina arista e."""
        e = self._validate_edge(e_uid)
        
        v1, v2 = e.endpoints()
        
        # Quitarla de los vértices
        v1._incoming.pop(e_uid, None)
        v1._outgoing.pop(e_uid, None)
        v2._incoming.pop(e_uid, None)
        v2._outgoing.pop(e_uid, None)
        
        # Quitarla del grafo
        del self._edges[e_uid]


# --- 2. CLASE DE LA APLICACIÓN GUI (CUSTOMTKINTER) ---

class GraphApp(ctk.CTk):
    
    VERTEX_RADIUS = 20
    NODE_COLOR = "#2b2b2b"
    NODE_HIGHLIGHT_COLOR = "#00AFFF" # Azul
    NODE_SECOND_COLOR = "#FFAF00" # Naranja
    EDGE_COLOR = "#303030" # Color más oscuro para mejor contraste
    EDGE_HIGHLIGHT_COLOR = "#00AFFF"
    TEXT_COLOR = "#FFFFFF"

    def __init__(self):
        super().__init__()
        
        self.title("Visualizador de Grafos sobre Mapa")
        self.geometry("1200x800")
        ctk.set_appearance_mode("Dark")
        
        self.graph = Graph()
        self.vertex_coords = {}  # {v_uid: (x, y)}
        self.vertex_elements = {} # {element: v_uid}
        
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # --- Variables para la imagen de fondo ---
        self.bg_image_original = None
        self.bg_image_tk = None
        self.bg_canvas_item = None

        # --- Layout Principal ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Frame de Controles (Izquierda) ---
        self.control_frame = ctk.CTkScrollableFrame(self, width=350)
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # --- Canvas de Dibujo (Derecha) ---
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Quitamos el color de fondo, la imagen lo reemplazará
        self.canvas = ctk.CTkCanvas(self.canvas_frame, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- Etiqueta de Resultados (Abajo) ---
        self.result_label = ctk.CTkLabel(self, text="Bienvenido al Visualizador de Grafos",
                                         font=ctk.CTkFont(size=14, weight="bold"))
        self.result_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # --- Poblar Controles ---
        self.setup_controls()
        
        # --- Bindeo para Drag-and-Drop ---
        self.canvas.tag_bind("vertex", "<ButtonPress-1>", self.on_vertex_press)
        self.canvas.tag_bind("vertex", "<B1-Motion>", self.on_vertex_drag)

        # --- ¡NUEVO! ---
        # --- Cargar la imagen de fondo y bindeo de redimensionar ---
        try:
            # Abrir la imagen original
            self.bg_image_original = Image.open("mapa_fondo.png")
            
            # Crear el item de imagen en el canvas
            self.bg_canvas_item = self.canvas.create_image(0, 0, anchor="nw")
            
            # Bindeo para que la imagen se redimensione con la ventana
            self.canvas.bind("<Configure>", self.on_canvas_resize)
            
        except FileNotFoundError:
            self.show_result("ADVERTENCIA: No se encontró 'mapa_fondo.png'. Se usará fondo gris.", is_error=True)
            self.canvas.configure(bg="#1c1c1c") # Fondo de fallback
            self.bg_image_original = None
        except Exception as e:
            self.show_result(f"Error cargando imagen: {e}", is_error=True)
            self.canvas.configure(bg="#1c1c1c")
            self.bg_image_original = None
        # --- FIN NUEVO ---

        # --- Cargar un grafo de ejemplo ---
        self.load_sample_graph()
        self.draw_graph()

    # --- ¡NUEVO! ---
    def on_canvas_resize(self, event):
        """Se activa cuando el canvas cambia de tamaño. Redimensiona la imagen de fondo."""
        if not self.bg_image_original:
            return # No hay imagen para redimensionar

        width = event.width
        height = event.height
        
        # Evitar redimensionar a 0x0 al inicio
        if width == 0 or height == 0:
            return

        # Redimensionar la imagen original (alta calidad)
        resized_image = self.bg_image_original.resize((width, height), Image.Resampling.LANCZOS)
        
        # Actualizar la imagen de PhotoImage (guardamos referencia)
        self.bg_image_tk = ImageTk.PhotoImage(resized_image)
        
        # Actualizar el item del canvas
        self.canvas.itemconfig(self.bg_canvas_item, image=self.bg_image_tk)
        self.canvas.coords(self.bg_canvas_item, 0, 0)
        self.canvas.lower(self.bg_canvas_item) # Asegurar que esté al fondo

    # --- Lógica de Dibujo ---

    def draw_graph(self, highlights={}):
        """Dibuja el grafo completo en el canvas.
        highlights = {"vertices": {v_uid: color}, "edges": {e_uid: color}}
        """
        
        # --- ¡MODIFICADO! ---
        # Ya no usamos self.canvas.delete("all") para no borrar el fondo
        self.canvas.delete("edge")
        self.canvas.delete("vertex")
        self.canvas.delete("vertex_text")
        # --- FIN MODIFICADO ---
        
        highlight_v = highlights.get("vertices", {})
        highlight_e = highlights.get("edges", {})

        # 1. Dibujar Aristas
        for e_uid, edge in self.graph._edges.items():
            v1, v2 = edge.endpoints()
            # Validar que ambas coordenadas existen antes de dibujar
            if v1._uid not in self.vertex_coords or v2._uid not in self.vertex_coords:
                continue
            
            x1, y1 = self.vertex_coords[v1._uid]
            x2, y2 = self.vertex_coords[v2._uid]
            
            color = highlight_e.get(e_uid, self.EDGE_COLOR)
            width = 3 if e_uid in highlight_e else 1.5
            
            # Usamos tags para poder borrarlos luego
            line_tags = ("edge", e_uid)
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, tags=line_tags)
            
            if edge._directed:
                # El tag 'edge' también se aplica a la flecha
                self._draw_arrow(x1, y1, x2, y2, color, line_tags)

        # 2. Dibujar Vértices (encima de las aristas)
        for v_uid, vertex in self.graph._vertices.items():
            if v_uid not in self.vertex_coords:
                continue # No dibujar si no tiene coords
                
            x, y = self.vertex_coords[v_uid]
            
            color = highlight_v.get(v_uid, self.NODE_COLOR)
            
            self.canvas.create_oval(
                x - self.VERTEX_RADIUS, y - self.VERTEX_RADIUS,
                x + self.VERTEX_RADIUS, y + self.VERTEX_RADIUS,
                fill=color, outline=color, tags=("vertex", "vertex_" + v_uid, v_uid)
            )
            self.canvas.create_text(
                x, y, text=str(vertex._element), fill=self.TEXT_COLOR,
                font=ctk.CTkFont(size=12, weight="bold"),
                tags=("vertex_text", "text_" + v_uid, v_uid)
            )
            
    # --- ¡NUEVO! ---
    # Modificado para aceptar tags
    def _draw_arrow(self, x1, y1, x2, y2, color, tags):
        """Dibuja una flecha al final de una línea."""
        size = 15
        try:
            angle = math.atan2(y2 - y1, x2 - x1)
        except ValueError:
            angle = 0 # Evitar crash si (x1,y1) == (x2,y2)
        
        # Calcular el punto final en el borde del círculo
        end_x = x2 - self.VERTEX_RADIUS * math.cos(angle)
        end_y = y2 - self.VERTEX_RADIUS * math.sin(angle)
        
        p1_x = end_x - size * math.cos(angle - math.pi / 6)
        p1_y = end_y - size * math.sin(angle - math.pi / 6)
        p2_x = end_x - size * math.cos(angle + math.pi / 6)
        p2_y = end_y - size * math.sin(angle + math.pi / 6)
        
        self.canvas.create_polygon(end_x, end_y, p1_x, p1_y, p2_x, p2_y, 
                                   fill=color, tags=tags)
    # --- FIN NUEVO ---


    # --- EL RESTO DE TU CÓDIGO ---
    # (setup_controls, load_sample_graph, Handlers de Drag-and-Drop,
    #  Handlers de Botones, etc. van aquí SIN CAMBIOS)
    def setup_controls(self):
        """Crea todos los botones y campos de entrada."""
        frame = self.control_frame
        row = 0

        # --- Entradas ---
        ctk.CTkLabel(frame, text="Parámetros:", font=ctk.CTkFont(weight="bold")).grid(row=row, column=0, columnspan=2, pady=(5, 5), sticky="w")
        row += 1
        
        ctk.CTkLabel(frame, text="Vértice v:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.entry_v = ctk.CTkEntry(frame, placeholder_text="Ej: A")
        self.entry_v.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        ctk.CTkLabel(frame, text="Vértice w:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.entry_w = ctk.CTkEntry(frame, placeholder_text="Ej: B")
        self.entry_w.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        ctk.CTkLabel(frame, text="Arista e:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.entry_e = ctk.CTkEntry(frame, placeholder_text="UID (ej: e0)")
        self.entry_e.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1
        
        ctk.CTkLabel(frame, text="Objeto o:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.entry_o = ctk.CTkEntry(frame, placeholder_text="Dato (ej: A)")
        self.entry_o.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1
        
        # --- Separador ---
        ctk.CTkLabel(frame, text="").grid(row=row, column=0)
        row += 1

        # --- Operaciones Generales ---
        ctk.CTkLabel(frame, text="Operaciones Generales", font=ctk.CTkFont(weight="bold")).grid(row=row, column=0, columnspan=2, pady=(10, 5), sticky="w")
        row += 1
        
        ctk.CTkButton(frame, text="numVertices()", command=self.on_numVertices).grid(row=row, column=0, padx=5, pady=3, sticky="ew")
        ctk.CTkButton(frame, text="numAristas()", command=self.on_numAristas).grid(row=row, column=1, padx=5, pady=3, sticky="ew")
        row += 1
        
        ctk.CTkButton(frame, text="vertices()", command=self.on_vertices).grid(row=row, column=0, padx=5, pady=3, sticky="ew")
        ctk.CTkButton(frame, text="aristas()", command=self.on_aristas).grid(row=row, column=1, padx=5, pady=3, sticky="ew")
        row += 1
        
        ctk.CTkButton(frame, text="grado(v)", command=self.on_grado).grid(row=row, column=0, padx=5, pady=3, sticky="ew")
        ctk.CTkButton(frame, text="verticesAdyacentes(v)", command=self.on_verticesAdyacentes).grid(row=row, column=1, padx=5, pady=3, sticky="ew")
        row += 1

        ctk.CTkButton(frame, text="aristasIncidentes(v)", command=self.on_aristasIncidentes).grid(row=row, column=0, padx=5, pady=3, sticky="ew")
        ctk.CTkButton(frame, text="verticesFinales(e)", command=self.on_verticesFinales).grid(row=row, column=1, padx=5, pady=3, sticky="ew")
        row += 1
        
        ctk.CTkButton(frame, text="opuesto(v, e)", command=self.on_opuesto).grid(row=row, column=0, padx=5, pady=3, sticky="ew")
        ctk.CTkButton(frame, text="esAdyacente(v, w)", command=self.on_esAdyacente).grid(row=row, column=1, padx=5, pady=3, sticky="ew")
        row += 1

        # --- Operaciones Dirigidas ---
        ctk.CTkLabel(frame, text="Operaciones Dirigidas", font=ctk.CTkFont(weight="bold")).grid(row=row, column=0, columnspan=2, pady=(10, 5), sticky="w")
        row += 1
        
        ctk.CTkButton(frame, text="aristasDirigidas()", command=self.on_aristasDirigidas).grid(row=row, column=0, padx=5, pady=3, sticky="ew")
        ctk.CTkButton(frame, text="aristasNodirigidas()", command=self.on_aristasNodirigidas).grid(row=row, column=1, padx=5, pady=3, sticky="ew")
        row += 1
        ctk.CTkButton(frame, text="gradoEnt(v)", command=self.on_gradoEnt).grid(row=row, column=0, padx=5, pady=3, sticky="ew")
        ctk.CTkButton(frame, text="gradoSalida(v)", command=self.on_gradoSalida).grid(row=row, column=1, padx=5, pady=3, sticky="ew")
        row += 1

        # --- Operaciones de Actualización ---
        ctk.CTkLabel(frame, text="Operaciones de Actualización", font=ctk.CTkFont(weight="bold")).grid(row=row, column=0, columnspan=2, pady=(10, 5), sticky="w")
        row += 1
        
        ctk.CTkButton(frame, text="insertaVertice(o)", command=self.on_insertaVertice, fg_color="green").grid(row=row, column=0, padx=5, pady=3, sticky="ew")
        ctk.CTkButton(frame, text="eliminaVertice(v)", command=self.on_eliminaVertice, fg_color="red").grid(row=row, column=1, padx=5, pady=3, sticky="ew")
        row += 1

        ctk.CTkButton(frame, text="insertaArista(v,w,o)", command=self.on_insertaArista, fg_color="green").grid(row=row, column=0, padx=5, pady=3, sticky="ew")
        ctk.CTkButton(frame, text="eliminaArista(e)", command=self.on_eliminaArista, fg_color="red").grid(row=row, column=1, padx=5, pady=3, sticky="ew")
        row += 1

        ctk.CTkButton(frame, text="insertaAristaDirigida(v,w,o)", command=self.on_insertaAristaDirigida, fg_color="green").grid(row=row, column=0, columnspan=2, padx=5, pady=3, sticky="ew")
        row += 1
        
        # --- Control ---
        ctk.CTkLabel(frame, text="").grid(row=row, column=0)
        row += 1
        ctk.CTkButton(frame, text="Limpiar Grafo", command=self.on_clear_graph, fg_color="#D35400").grid(row=row, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        row += 1


    def load_sample_graph(self):
        """Carga un grafo simple para demostración."""
        self.on_clear_graph()
        try:
            # Estas coordenadas ahora se dibujarán SOBRE el mapa
            vA = self.graph.insertaVertice("A")
            vB = self.graph.insertaVertice("B")
            vC = self.graph.insertaVertice("C")
            vD = self.graph.insertaVertice("D")
            
            self.vertex_coords[vA] = (100, 100)
            self.vertex_coords[vB] = (300, 150)
            self.vertex_coords[vC] = (100, 300)
            self.vertex_coords[vD] = (400, 350)
            
            self.vertex_elements = {"A": vA, "B": vB, "C": vC, "D": vD}

            self.graph.insertaArista(vA, vB, "e_AB")
            self.graph.insertaArista(vA, vC, "e_AC")
            self.graph.insertaAristaDirigida(vB, vC, "e_BC")
            self.graph.insertaAristaDirigida(vC, vD, "e_CD")
        except Exception as e:
            self.show_result(f"Error cargando grafo: {e}", is_error=True)
            
    # --- Handlers de Drag-and-Drop ---

    def on_vertex_press(self, event):
        """Inicia el arrastre de un vértice."""
        v_tag = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(v_tag)
        v_uid = None
        for t in tags:
            if t.startswith("v"): 
                v_uid = t
                break
        
        if v_uid and v_uid in self.vertex_coords:
            self._drag_data["item"] = v_uid
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y

    def on_vertex_drag(self, event):
        """Mueve el vértice mientras se arrastra."""
        if self._drag_data["item"]:
            v_uid = self._drag_data["item"]
            dx = event.x - self._drag_data["x"]
            dy = event.y - self._drag_data["y"]
            
            self.canvas.move("vertex_" + v_uid, dx, dy)
            self.canvas.move("text_" + v_uid, dx, dy)
            
            self.vertex_coords[v_uid] = (self.vertex_coords[v_uid][0] + dx, 
                                         self.vertex_coords[v_uid][1] + dy)
            
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
            
            # Redibujamos solo el grafo, el fondo no se mueve
            self.draw_graph()

    # --- Handlers de Botones (Visualización) ---
    
    def _get_vertex_uid_from_entry(self, entry_widget):
        """Helper para obtener UID desde el elemento en la entrada."""
        element = entry_widget.get()
        if not element:
            self.show_result("Error: El campo del vértice está vacío.", is_error=True)
            return None
        
        v_uid = self.vertex_elements.get(element)
        if not v_uid:
            self.show_result(f"Error: Vértice '{element}' no encontrado.", is_error=True)
            return None
        return v_uid
    
    def _reset_visual(self):
        """Resetea el grafo a su estado normal después de una visualización."""
        self.draw_graph()
        
    def show_result(self, message, is_error=False):
        """Muestra un mensaje en la etiqueta de resultados."""
        if is_error:
            self.result_label.configure(text=message, text_color="#FF5555")
        else:
            self.result_label.configure(text=message, text_color="white")

    # --- IMPLEMENTADOS CON VISUALIZACIÓN ---

    def on_insertaVertice(self):
        """Visualiza la inserción de un vértice."""
        element = self.entry_o.get()
        if not element:
            self.show_result("Error: Debe ingresar un 'Objeto o' (nombre) para el vértice.", is_error=True)
            return
        if element in self.vertex_elements:
            self.show_result(f"Error: El vértice '{element}' ya existe.", is_error=True)
            return

        try:
            # Colocar en un lugar aleatorio
            x = random.randint(self.VERTEX_RADIUS + 10, self.canvas.winfo_width() - self.VERTEX_RADIUS - 10)
            y = random.randint(self.VERTEX_RADIUS + 10, self.canvas.winfo_height() - self.VERTEX_RADIUS - 10)
            
            v_uid = self.graph.insertaVertice(element)
            self.vertex_coords[v_uid] = (x, y)
            self.vertex_elements[element] = v_uid
            
            self.draw_graph(highlights={"vertices": {v_uid: "green"}})
            self.show_result(f"Vértice '{element}' (UID: {v_uid}) insertado.")
            
            self.after(2000, self._reset_visual)
            
        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)

    def on_insertaArista(self, dirigida=False):
        """Visualiza la inserción de una arista (dirigida o no)."""
        v_uid = self._get_vertex_uid_from_entry(self.entry_v)
        w_uid = self._get_vertex_uid_from_entry(self.entry_w)
        o = self.entry_o.get() or None # 'None' si está vacío
        
        if not v_uid or not w_uid:
            return 
            
        try:
            if dirigida:
                e_uid = self.graph.insertaAristaDirigida(v_uid, w_uid, o)
                msg = f"Arista dirigida '{o or e_uid}' insertada de {self.entry_v.get()} a {self.entry_w.get()}."
            else:
                e_uid = self.graph.insertaArista(v_uid, w_uid, o)
                msg = f"Arista no dirigida '{o or e_uid}' insertada entre {self.entry_v.get()} y {self.entry_w.get()}."

            self.draw_graph(highlights={"edges": {e_uid: "green"}})
            self.show_result(msg)
            self.after(2000, self._reset_visual)

        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)

    def on_insertaAristaDirigida(self):
        self.on_insertaArista(dirigida=True)

    def on_eliminaVertice(self):
        """Visualiza la eliminación de un vértice."""
        v_uid = self._get_vertex_uid_from_entry(self.entry_v)
        if not v_uid:
            return

        try:
            element = self.entry_v.get()
            aristas_a_eliminar = self.graph.aristasIncidentes(v_uid)
            
            h_v = {v_uid: "red"}
            h_e = {e_uid: "red" for e_uid in aristas_a_eliminar}
            
            self.draw_graph(highlights={"vertices": h_v, "edges": h_e})
            self.show_result(f"Eliminando vértice '{element}' y {len(aristas_a_eliminar)} aristas incidentes...")
            
            def do_delete():
                self.graph.eliminaVertice(v_uid)
                # También eliminar de nuestros diccionarios de GUI
                if v_uid in self.vertex_coords:
                    del self.vertex_coords[v_uid]
                if element in self.vertex_elements:
                    del self.vertex_elements[element]
                    
                self.draw_graph()
                self.show_result(f"Vértice '{element}' eliminado.")
                
            self.after(2000, do_delete)

        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)

    def on_eliminaArista(self):
        e_uid = self.entry_e.get()
        if not e_uid:
            self.show_result("Error: Debe ingresar un 'UID de Arista e'.", is_error=True)
            return
            
        try:
            self.graph._validate_edge(e_uid)
            
            self.draw_graph(highlights={"edges": {e_uid: "red"}})
            self.show_result(f"Eliminando arista '{e_uid}'...")
            
            def do_delete():
                self.graph.eliminaArista(e_uid)
                self.draw_graph()
                self.show_result(f"Arista '{e_uid}' eliminada.")
                
            self.after(2000, do_delete)
        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)


    def on_grado(self):
        """Visualiza las aristas que contribuyen al grado de v."""
        v_uid = self._get_vertex_uid_from_entry(self.entry_v)
        if not v_uid:
            return
        
        try:
            grado = self.graph.grado(v_uid)
            aristas_incidentes = self.graph.aristasIncidentes(v_uid)
            
            h_v = {v_uid: self.NODE_HIGHLIGHT_COLOR}
            h_e = {e_uid: self.EDGE_HIGHLIGHT_COLOR for e_uid in aristas_incidentes}
            
            self.draw_graph(highlights={"vertices": h_v, "edges": h_e})
            self.show_result(f"grado({self.entry_v.get()}) = {grado}")
            self.after(3000, self._reset_visual)
            
        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)

    def on_verticesAdyacentes(self):
        """Visualiza los vértices adyacentes a v."""
        v_uid = self._get_vertex_uid_from_entry(self.entry_v)
        if not v_uid:
            return

        try:
            adyacentes_uids = self.graph.verticesAdyacentes(v_uid)
            aristas_incidentes = self.graph.aristasIncidentes(v_uid)
            
            h_v = {v_uid: self.NODE_HIGHLIGHT_COLOR}
            for uid in adyacentes_uids:
                h_v[uid] = self.NODE_SECOND_COLOR
                
            h_e = {e_uid: self.EDGE_HIGHLIGHT_COLOR for e_uid in aristas_incidentes}
            
            self.draw_graph(highlights={"vertices": h_v, "edges": h_e})
            
            adyacentes_elements = [self.graph.get_vertex_element(uid) for uid in adyacentes_uids]
            self.show_result(f"verticesAdyacentes({self.entry_v.get()}) = {adyacentes_elements}")
            self.after(3000, self._reset_visual)

        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)

    # --- STUBS (Sin visualización, solo muestran resultado) ---
    
    def on_numVertices(self):
        num = self.graph.numVertices()
        self.show_result(f"numVertices() = {num}")
        self.draw_graph(highlights={"vertices": {v_uid: self.NODE_HIGHLIGHT_COLOR for v_uid in self.graph.vertices()}})
        self.after(2000, self._reset_visual)

    def on_numAristas(self):
        num = self.graph.numAristas()
        self.show_result(f"numAristas() = {num}")
        self.draw_graph(highlights={"edges": {e_uid: self.EDGE_HIGHLIGHT_COLOR for e_uid in self.graph.aristas()}})
        self.after(2000, self._reset_visual)

    def on_vertices(self):
        v_list = self.graph.vertices()
        self.show_result(f"vertices() = {v_list}")
        self.draw_graph(highlights={"vertices": {v_uid: self.NODE_HIGHLIGHT_COLOR for v_uid in v_list}})
        self.after(2000, self._reset_visual)

    def on_aristas(self):
        e_list = self.graph.aristas()
        self.show_result(f"aristas() = {e_list}")
        self.draw_graph(highlights={"edges": {e_uid: self.EDGE_HIGHLIGHT_COLOR for e_uid in e_list}})
        self.after(2000, self._reset_visual)

    def on_aristasIncidentes(self):
        v_uid = self._get_vertex_uid_from_entry(self.entry_v)
        if not v_uid: return
        try:
            aristas = self.graph.aristasIncidentes(v_uid)
            self.show_result(f"aristasIncidentes({self.entry_v.get()}) = {aristas}")
            h_v = {v_uid: self.NODE_HIGHLIGHT_COLOR}
            h_e = {e_uid: self.EDGE_HIGHLIGHT_COLOR for e_uid in aristas}
            self.draw_graph(highlights={"vertices": h_v, "edges": h_e})
            self.after(3000, self._reset_visual)
        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)

    def on_verticesFinales(self):
        e_uid = self.entry_e.get()
        if not e_uid:
            self.show_result("Error: Debe ingresar un 'UID de Arista e'.", is_error=True)
            return
        try:
            v1, v2 = self.graph.verticesFinales(e_uid)
            v1_elem = self.graph.get_vertex_element(v1)
            v2_elem = self.graph.get_vertex_element(v2)
            self.show_result(f"verticesFinales({e_uid}) = ({v1_elem}, {v2_elem})")
            h_v = {v1: self.NODE_SECOND_COLOR, v2: self.NODE_SECOND_COLOR}
            h_e = {e_uid: self.EDGE_HIGHLIGHT_COLOR}
            self.draw_graph(highlights={"vertices": h_v, "edges": h_e})
            self.after(3000, self._reset_visual)
        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)

    def on_opuesto(self):
        v_uid = self._get_vertex_uid_from_entry(self.entry_v)
        e_uid = self.entry_e.get()
        if not v_uid or not e_uid: return
        try:
            op_uid = self.graph.opuesto(v_uid, e_uid)
            op_elem = self.graph.get_vertex_element(op_uid)
            self.show_result(f"opuesto({self.entry_v.get()}, {e_uid}) = {op_elem} (UID: {op_uid})")
            
            h_v = {v_uid: self.NODE_HIGHLIGHT_COLOR, op_uid: self.NODE_SECOND_COLOR}
            h_e = {e_uid: self.EDGE_HIGHLIGHT_COLOR}
            self.draw_graph(highlights={"vertices": h_v, "edges": h_e})
            self.after(3000, self._reset_visual)
        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)

    def on_esAdyacente(self):
        v_uid = self._get_vertex_uid_from_entry(self.entry_v)
        w_uid = self._get_vertex_uid_from_entry(self.entry_w)
        if not v_uid or not w_uid: return
        try:
            resultado = self.graph.esAdyacente(v_uid, w_uid)
            self.show_result(f"esAdyacente({self.entry_v.get()}, {self.entry_w.get()}) = {resultado}")
            
            h_v = {v_uid: self.NODE_HIGHLIGHT_COLOR, w_uid: self.NODE_HIGHLIGHT_COLOR}
            self.draw_graph(highlights={"vertices": h_v})
            self.after(3000, self._reset_visual)
        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)

    # --- Handlers para Métodos Dirigidos (Stubs) ---
    def on_aristasDirigidas(self):
        aristas = self.graph.aristasDirigidas()
        self.show_result(f"aristasDirigidas() = {aristas}")
        self.draw_graph(highlights={"edges": {e_uid: self.EDGE_HIGHLIGHT_COLOR for e_uid in aristas}})
        self.after(2000, self._reset_visual)

    def on_aristasNodirigidas(self):
        aristas = self.graph.aristasNodirigidas()
        self.show_result(f"aristasNodirigidas() = {aristas}")
        self.draw_graph(highlights={"edges": {e_uid: self.EDGE_HIGHLIGHT_COLOR for e_uid in aristas}})
        self.after(2000, self._reset_visual)

    def on_gradoEnt(self):
        v_uid = self._get_vertex_uid_from_entry(self.entry_v)
        if not v_uid: return
        try:
            grado = self.graph.gradoEnt(v_uid)
            aristas = self.graph.aristasIncidentesEnt(v_uid)
            self.show_result(f"gradoEnt({self.entry_v.get()}) = {grado}")
            h_v = {v_uid: self.NODE_HIGHLIGHT_COLOR}
            h_e = {e_uid: self.EDGE_HIGHLIGHT_COLOR for e_uid in arISTAS}
            self.draw_graph(highlights={"vertices": h_v, "edges": h_e})
            self.after(3000, self._reset_visual)
        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)

    def on_gradoSalida(self):
        v_uid = self._get_vertex_uid_from_entry(self.entry_v)
        if not v_uid: return
        try:
            grado = self.graph.gradoSalida(v_uid)
            aristas = self.graph.aristasIncidentesSal(v_uid)
            self.show_result(f"gradoSalida({self.entry_v.get()}) = {grado}")
            h_v = {v_uid: self.NODE_HIGHLIGHT_COLOR}
            h_e = {e_uid: self.EDGE_HIGHLIGHT_COLOR for e_uid in aristas}
            self.draw_graph(highlights={"vertices": h_v, "edges": h_e})
            self.after(3000, self._reset_visual)
        except Exception as e:
            self.show_result(f"Error: {e}", is_error=True)


    # --- Otros ---
    
    def on_clear_graph(self):
        """Limpia el grafo y el canvas."""
        self.graph = Graph()
        self.vertex_coords = {}
        self.vertex_elements = {}
        # No borramos el fondo, solo los items del grafo
        self.draw_graph()
        self.show_result("Grafo limpiado.")


# --- 3. EJECUCIÓN DE LA APP ---

if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()