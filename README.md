<p align="center">
  <img alt="OSMnx" src="https://img.shields.io/badge/OSMnx-2.0.3-brightgreen?logo=openstreetmap&logoColor=white" />
  <img alt="Folium" src="https://img.shields.io/badge/Folium-0.19.5-blue?logo=leaflet&logoColor=white" />
</p>


# OrbiTrack_Python 🚀

¡Pon tus rutas en órbita con Python y humor! 😄

## 📡 ¿Qué es OrbiTrack_Python?
Un script que:
- Descarga calles de Lima con **OSMnx**.
- Construye un grafo de nodos y aristas.
- Resuelve el TSP exacto con **Held-Karp**.
- Genera un mapa interactivo en HTML con **Folium**.

## 🌟 Características
- **Datos de Lima**: obtenidos al vuelo de OpenStreetMap.  
- **Algoritmo óptimo**: Held-Karp para rutas exactas (ideal para ≤10 puntos).  
- **Visualización**: mapa HTML con marcadores y ruta trazada.  
- **CSV listo**: `lima_nodes.csv` y `lima_edges.csv` para tu propio análisis.

## 🛠️ Instalación
1. Clona el repo:
   ```bash
   git clone https://github.com/AlexC0dex/OrbiTrack_Python.git
   cd OrbiTrack_Python

2. (Opcional) Entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Instala dependencias:

   ```bash
   pip install osmnx folium pandas
   ```
4. Asegúrate de tener **internet** para descargar el mapa.

## 🚴‍♂️ Uso rápido

1. **Extrae datos**:

   ```bash
   python data_html.py
   ```

   — Genera `lima_nodes.csv` y `lima_edges.csv`.
2. **Calcula ruta**:

   ```bash
   python ruta_optima.py
   ```

   — Crea `lima_streets_map_tsp_exact.html`.
3. **Abre el HTML** en tu navegador y disfruta de la ruta óptima:

## 📝 Ejemplo

Por defecto, el script selecciona varios puntos en Lima (Plaza Mayor, Miraflores, Barranco…) y traza la ruta más corta que los conecta todos. 🎉

¡Que tus rutas siempre sean óptimas! 🚀

