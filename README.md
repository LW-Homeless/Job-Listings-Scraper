# Job Listings Scraper

Aplicación de terminal (TUI) construida con **Python** y **Textual** que extrae ofertas de empleo desde el sitio [Fake Python Jobs](https://realpython.github.io/fake-jobs/), mostrando los resultados en vivo en una tabla interactiva mientras se ejecuta el scraping.

Proyecto desarrollado como solución al desafío **[Python Job Listings Scraper](https://roadmap.sh/projects/job-listings-scraper)** de [roadmap.sh](https://roadmap.sh/).

## Demo
![Demo de la aplicación](https://github.com/LW-Homeless/Job-Listings-Scraper/blob/main/job-scraper.gif?raw=true)

## Características

- 🔎 Extrae automáticamente, para cada oferta de empleo:
  - Título del puesto
  - Nombre de la empresa
  - Ubicación
  - URL de detalle de la oferta
- 📊 Tabla de resultados que se actualiza en tiempo real conforme se procesa cada oferta
- 📋 Panel de logs con el progreso del proceso (links encontrados, estado, errores)
- 📈 Barra de progreso durante la extracción de datos
- 🎭 Rotación de User-Agent en cada petición HTTP
- ⚠️ Manejo de errores de conexión y de elementos faltantes en el HTML

## Tecnologías utilizadas

- **[Python](https://www.python.org/)** 3.14
- **[Textual](https://textual.textualize.io/)** – framework para construir la interfaz de terminal (TUI)
- **[Requests](https://requests.readthedocs.io/)** – para realizar las peticiones HTTP
- **[Beautiful Soup (bs4)](https://www.crummy.com/software/BeautifulSoup/)** – para analizar y recorrer el HTML

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/LW-Homeless/Job-Listings-Scraper.git
   ```

2. Crea y activa un entorno virtual (opcional, pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecuta la aplicación:

```bash
python app.py
```

### Atajos de teclado

| Tecla | Acción                  |
|-------|--------------------------|
| `s`   | Ejecutar el scraper       |
| `q`   | Cerrar la aplicación      |

Al presionar `s`, la aplicación:

1. Obtiene todos los links de ofertas de empleo desde la página principal.
2. Visita cada oferta individualmente para extraer título, empresa, ubicación y URL de detalle.
3. Va actualizando la tabla de resultados en tiempo real, junto con una barra de progreso.

## Cómo funciona

- **`Request`**: encapsula las peticiones HTTP con `requests`, asignando un User-Agent aleatorio en cada instancia para evitar bloqueos.
- **`Scraper`**: recibe el HTML crudo y lo convierte en un objeto navegable de BeautifulSoup para poder buscar elementos.
- **`MainScreen`**: orquesta el flujo completo — obtiene los links, realiza el scraping oferta por oferta, y actualiza la interfaz (tabla, logs y barra de progreso) de forma asíncrona.

## Aprendizajes del proyecto

Este proyecto puso en práctica:

- Inspección de la estructura HTML de una página real para identificar patrones reutilizables.
- Extracción de datos estructurados con Beautiful Soup (`find`, `find_all`, filtrado por clase/id).
- Manejo de errores de red y de elementos HTML ausentes.
- Construcción de una interfaz de terminal interactiva y asíncrona con Textual.
- Actualización de UI en tiempo real durante tareas de larga duración (`async`/`await`).
