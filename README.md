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
├── flight_log.csv
└── README.md

"flight_log.csv" se genera al ejecutar el programa generador.

3. Componentes

generate_flight.py

Genera datos simulados de vuelo, incluyendo:

- Tiempo de muestreo.
- Altitud.
- Aceleración en el eje Z.
- Temperatura.

Los datos se guardan en un archivo CSV llamado "flight_log.csv".

process_flight.py

Procesa el archivo CSV mediante las siguientes operaciones:

- Lectura y validación de registros.
- Identificación y descarte de datos inválidos.
- Aplicación de filtros de media móvil de 5 y 15 muestras.
- Cálculo de velocidad vertical.
- Detección de eventos de vuelo: despegue, apogeo y aterrizaje.

4. Requisitos

- Python 3.
- No requiere bibliotecas externas.

5. Ejecución

Desde el directorio principal del repositorio, ejecutar primero:

python src/generate_flight.py

Después, ejecutar:

python src/process_flight.py

El primer programa genera el archivo "flight_log.csv" y el segundo lo utiliza para realizar el procesamiento.

6. Resultado esperado

El procesamiento presenta un resumen con:

- Cantidad de registros válidos y descartados.
- Resultados de los filtros de media móvil.
- Velocidades verticales calculadas.
- Tiempos de detección de despegue, apogeo y aterrizaje.
- Altitud máxima registrada.

Los resultados corresponden a una simulación de vuelo y pueden variar si se modifican los parámetros de generación.

7. Alcance

Esta etapa corresponde al desarrollo de un sistema inicial de generación y procesamiento de telemetría de vuelo. Los resultados permiten evaluar el funcionamiento de los procedimientos de depuración, filtrado y detección de eventos.