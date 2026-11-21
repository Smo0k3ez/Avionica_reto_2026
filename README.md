Avionica_reto_2026

Sistema de generación y procesamiento de datos de vuelo

Proyecto desarrollado para el Reto de Reclutamiento de la División de Aviónica de la AAIAQ, noviembre de 2026.

1. Descripción del proyecto

Este proyecto implementa un sistema básico de simulación y procesamiento de datos de vuelo. Su objetivo es generar un registro de telemetría simulado y procesarlo para obtener información relevante sobre el comportamiento del vuelo.

2. Estructura del proyecto

Avionica_reto_2026/
│
├── src/
│   ├── generate_flight.py
│   └── process_flight.py
│
├── README.md
├── altitude_plot.png
└── velocity_plot.png

Los archivos CSV se generan durante la ejecución de los programas.

3. Componentes

generate_flight.py

Genera datos simulados de vuelo, incluyendo:

- Tiempo de muestreo.
- Altitud.
- Aceleración en el eje Z.
- Temperatura.

Los datos se guardan en "flight_log.csv".

process_flight.py

Procesa el archivo CSV mediante:

- Lectura y validación de registros.
- Identificación y descarte de datos inválidos.
- Aplicación de filtros de media móvil de 5 y 15 muestras.
- Cálculo de velocidad vertical.
- Detección de despegue, apogeo y aterrizaje.
- Cálculo de métricas del vuelo.
- Exportación de datos procesados y generación de gráficas.

4. Requisitos

- Python 3.
- Matplotlib.

Instalar Matplotlib mediante:

pip install matplotlib

5. Ejecución

Desde el directorio principal del repositorio, ejecutar primero:

python src/generate_flight.py

Después ejecutar:

python src/process_flight.py

6. Resultados generados

- "flight_log.csv": registro original de telemetría.
- "flight_processed.csv": datos procesados y filtrados.
- "altitude_plot.png": gráfica de altitud respecto al tiempo.
- "velocity_plot.png": gráfica de velocidad vertical respecto al tiempo.

El procesamiento también presenta un resumen de registros válidos y descartados, filtros aplicados, velocidades calculadas y eventos detectados.

7. Alcance

Esta etapa corresponde al desarrollo de un sistema inicial de generación y procesamiento de telemetría de vuelo. Los resultados permiten evaluar el funcionamiento de los procedimientos de depuración, filtrado, cálculo de velocidades y detección de eventos.