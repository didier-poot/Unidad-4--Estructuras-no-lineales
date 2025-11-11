import geopandas as gpd
import matplotlib.pyplot as plt
import os

# --- Construir la ruta absoluta (esta parte ya la tienes bien) ---
current_directory = os.getcwd()
file_name = "mexico.json"  # <-- El nombre con el backtick que descubriste
file_path = os.path.join(current_directory, file_name)


try:
    print("Cargando archivo (esto puede tardar unos segundos)...")
    municipios = gpd.read_file(file_path)
    
    print("Archivo cargado. Uniendo municipios para crear estados...")
    mexico_states = municipios.dissolve(by='NOM_ENT')
    
    print("¡Listo! Mostrando el mapa.")

    # 4. --- Graficar ---
    fig, ax = plt.subplots(1, 1, figsize=(10, 12)) 
    
    # 5. Dibujar el mapa de estados ya unidos
    mexico_states.plot(ax=ax, cmap='Greens', edgecolor='white', linewidth=0.5)

    # 6. --- ¡NUEVO! AÑADIR LOS NOMBRES DE LOS ESTADOS ---
    # Iteramos sobre cada fila (estado) del GeoDataFrame
    for idx, row in mexico_states.iterrows():
        
        # 'idx' es el nombre del estado (ej. "Yucatán")
        # 'row.geometry.representative_point()' nos da un punto (x, y) 
        # garantizado que está dentro del estado.
        label_point = row.geometry.representative_point()
        
        ax.text(
            x=label_point.x,
            y=label_point.y,
            s=idx,  # El texto que queremos escribir (el nombre del estado)
            ha='center',  # Alineación horizontal centrada
            va='center',  # Alineación vertical centrada
            fontsize=6,   # Tamaño de letra (ajusta si es muy grande/pequeño)
            color='black' # Color de la letra
        )
    # --- FIN DE LA SECCIÓN NUEVA ---

    # 7. --- Mejorar la visualización ---
    ax.set_title("Mapa Político de los Estados de México", fontsize=16)
    ax.set_axis_off() 

    # 8. Mostrar el gráfico
    plt.show()

except FileNotFoundError:
    print(f"--- ¡ERROR! ---")
    print(f"No se encontró el archivo en la ruta: '{file_path}'")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")