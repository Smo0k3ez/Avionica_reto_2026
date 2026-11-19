import csv
import math
import random

# ==========================================
# AAIAQ - DIVISION DE AVIONICA
# RUTA 1: TELEMETRIA
# Generador de datos de vuelo
# ==========================================

# Parametros de simulacion
FS = 10
DT = 1 / FS
G = 9.81

THRUST_TIME = 1.5
NET_ACCELERATION = 60.0
DESCENT_SPEED = 6.0

NOISE_STD = 0.5
GROUND_TEMP = 20.0

OUTPUT_FILE = "flight_log.csv"

random.seed(42)

# ==========================================
# CALCULOS DEL PERFIL DE VUELO
# ==========================================

# Fin de propulsion
burn_time = 2.0 + THRUST_TIME

# Velocidad al terminar propulsion
burn_velocity = NET_ACCELERATION * THRUST_TIME

# Altitud al terminar propulsion
burn_altitude = (
    0.5 * NET_ACCELERATION * THRUST_TIME**2
)

# Tiempo de ascenso balistico
coast_time = burn_velocity / G

# Altitud maxima teorica
apogee = (
    burn_altitude
    + burn_velocity**2 / (2 * G)
)

apogee_time = burn_time + coast_time

# Tiempo de descenso con paracaidas
descent_time = apogee / DESCENT_SPEED

landing_time = apogee_time + descent_time

# Duracion total incluyendo 3 segundos en tierra
total_time = landing_time + 3.0

# Numero de muestras a 10 Hz
total_samples = math.ceil(total_time * FS) + 1

# ==========================================
# GENERACION DE DATOS
# ==========================================

flight_data = []

for i in range(total_samples):

    time_s = i * DT
    time_ms = i * 100

    # FASE 1: EN RAMPA
    if time_s < 2.0:

        altitude = 0.0
        velocity = 0.0
        accel_z = G

    # FASE 2: PROPULSION
    elif time_s < burn_time:

        tau = time_s - 2.0

        altitude = (
            0.5 * NET_ACCELERATION * tau**2
        )

        velocity = NET_ACCELERATION * tau

        accel_z = NET_ACCELERATION + G

    # FASE 3: VUELO BALISTICO
    elif time_s < apogee_time:

        tau = time_s - burn_time

        altitude = (
            burn_altitude
            + burn_velocity * tau
            - 0.5 * G * tau**2
        )

        velocity = burn_velocity - G * tau

        accel_z = 0.0

    # FASE 4: DESCENSO CON PARACAIDAS
    elif time_s < landing_time:

        tau = time_s - apogee_time

        altitude = max(
            0.0,
            apogee - DESCENT_SPEED * tau
        )

        velocity = -DESCENT_SPEED
        accel_z = G

    # FASE 5: EN TIERRA
    else:

        altitude = 0.0
        velocity = 0.0
        accel_z = G

    # Ruido gaussiano en altitud
    measured_altitude = (
        altitude + random.gauss(0, NOISE_STD)
    )

    # Temperatura dependiente de la altitud real
    temperature = GROUND_TEMP - 0.0065 * altitude

    flight_data.append([
        time_ms,
        round(measured_altitude, 3),
        round(accel_z, 3),
        round(temperature, 3)
    ])

# ==========================================
# INSERCION DE TRES REGISTROS CORRUPTOS
# ==========================================

# Registro 1: campo vacio
flight_data[10][1] = ""

# Registro 2: dato no numerico
flight_data[40][1] = "ERR"

# Registro 3: columna faltante
flight_data[100] = flight_data[100][:3]

# ==========================================
# EXPORTACION CSV
# ==========================================

with open(OUTPUT_FILE, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "time_ms",
        "altitude_m",
        "accel_z_ms2",
        "temp_c"
    ])

    writer.writerows(flight_data)

# ==========================================
# RESUMEN
# ==========================================

print("SIMULACION DE VUELO COMPLETADA")
print("--------------------------------")
print("Frecuencia:", FS, "Hz")
print("Intervalo:", DT, "s")
print("Apogeo teorico:", round(apogee, 2), "m")
print("Tiempo de apogeo:", round(apogee_time, 2), "s")
print("Tiempo de aterrizaje:", round(landing_time, 2), "s")
print("Muestras generadas:", total_samples)
print("Registros corruptos: 3")
print("Archivo generado:", OUTPUT_FILE)
