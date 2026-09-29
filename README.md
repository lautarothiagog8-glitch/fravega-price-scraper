# Frávega Price Scraper (API Endpoint Scraper)

Scraper automatizado desarrollado en Python para extraer datos del catálogo de productos de Frávega interceptando directamente su API GraphQL/REST interna.

## Características
- **Paginación dinámica:** Recorre todo el catálogo mediante offsets dinámicos.
- **Sin navegador pesado:** Realiza solicitudes HTTP directas mediante `requests`, optimizando velocidad y memoria.
- **Estrategia Anti-Bot:** Implementa rotación aleatoria de `User-Agent` y pausas variables de cortesía (`rate limiting`).
- **Resiliente a errores:** Manejo explícito de excepciones HTTP (`403 Forbidden`, `429 Too Many Requests`, falta de conexión).
- **Gestión de rutas dinámicas:** Utiliza `pathlib` para garantizar compatibilidad multiplataforma.
- **Exportación organizada:** Guarda los resultados en un archivo CSV estructurado dentro de una carpeta organizadora con timestamp de ejecución.

## Estructura del CSV generado
| Fecha | Busqueda | Titulo | Precio |
|---|---|---|---|
| 27-09-2026_01-45-00 | mesas | Mesa Comedor Eames Madera | $125.000 |

## Instalación y Uso

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/lautarothiagog8-glitch/fravega-price-scraper.git
2. Instalar dependencias:
    ```bash
    pip install -r requirements.txt

3. Ejecutar el script:
    ```bash
    python main.py
