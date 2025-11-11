import geopandas as gpd
import matplotlib.pyplot as plt
import os

# --- Ajusta esta parte ---
# Asegúrate de que el archivo `mexico.json` (con el backtick) esté 
# en la misma carpeta donde ejecutes este script, o pon la ruta completa.
file_name = "mexico.json"
# -------------------------

try:
    print("Cargando archivo (esto puede tardar)...")
    municipios = gpd.read_file(file_name)
    
    print("Uniendo municipios...")
    mexico_states = municipios.dissolve(by='NOM_ENT')
    
    print("Generando gráfico...")
    
    # --- Configuración del gráfico ---
    # Queremos un mapa limpio, sin ejes ni fondo, solo los estados.
    fig, ax = plt.subplots(1, 1, figsize=(10, 12))
    
    # Dibujar con colores claros y bordes blancos
    mexico_states.plot(ax=ax, cmap='Pastel2', edgecolor='white', linewidth=0.5)

    # --- Limpiar todo ---
    ax.set_axis_off() 
    fig.patch.set_alpha(0) # Fondo de la figura transparente
    ax.patch.set_alpha(0)  # Fondo de los ejes transparente

    # --- Guardar la imagen ---
    output_filename = "mapa_fondo.png"
    plt.savefig(output_filename, 
                bbox_inches='tight',  # Ajustar al contenido
                pad_inches=0,         # Sin relleno
                transparent=True,     # Fondo transparente
                dpi=150)              # Buena resolución
    
    print(f"\n¡Éxito! Se ha guardado el mapa en '{output_filename}'.")
    print("Ya puedes usar este archivo en tu app de grafos.")

except FileNotFoundError:
    print(f"--- ¡ERROR! ---")
    print(f"No se encontró el archivo: '{file_name}'")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")