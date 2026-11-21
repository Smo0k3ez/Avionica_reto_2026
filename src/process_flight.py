import csv

# ==========================================
# AAIAQ - DIVISION DE AVIONICA
# RUTA 1: TELEMETRIA
# Procesamiento de datos de vuelo
# ==========================================

INPUT_FILE = "flight_log.csv"

# Listas para almacenar los datos validos
time_ms = []
altitude = []
accel_z = []
temperature = []

# Contadores de registros descartados
empty_records = 0
error_records = 0
missing_columns = 0

# ==========================================
# LECTURA Y VALIDACION DEL CSV
# ==========================================

with open(INPUT_FILE, "r", newline="") as file:

    reader = csv.reader(file)

    header = next(reader)

    for row in reader:

        # Comprobar columnas faltantes
        if len(row) != 4:
            missing_columns += 1
            continue

        # Comprobar campos vacios
        if "" in row:
            empty_records += 1
            continue

        # Comprobar datos no numericos
        try:
            t = float(row[0])
            h = float(row[1])
            a = float(row[2])
            temp = float(row[3])

        except ValueError:
            error_records += 1
            continue

        # Almacenar solamente registros validos
        time_ms.append(t)
        altitude.append(h)
        accel_z.append(a)
        temperature.append(temp)

# ==========================================
# RESUMEN DE DEPURACION
# ==========================================

total_discarded = (
    empty_records + error_records + missing_columns
)

print("LECTURA Y DEPURACION COMPLETADAS")
print("--------------------------------")
print("Registros validos:", len(time_ms))
print("Campos vacios descartados:", empty_records)
print("Registros no numericos:", error_records)
print("Registros con columnas faltantes:", missing_columns)
print("Total descartados:", total_discarded)

# ==========================================
# FILTROS DE MEDIA MOVIL
# ==========================================

def moving_average(data, window):

    filtered = []

    for i in range(len(data)):

        start = max(0, i - window + 1)

        total = 0

        for j in range(start, i + 1):
            total += data[j]

        average = total / (i - start + 1)

        filtered.append(average)

    return filtered


# Aplicar filtros N=5 y N=15

altitude_filtered_5 = moving_average(altitude, 5)

altitude_filtered_15 = moving_average(altitude, 15)


# ==========================================
# RESUMEN DE FILTRADO
# ==========================================

print("\nFILTROS DE MEDIA MOVIL")
print("--------------------------------")

print("Muestras filtradas N=5:", len(altitude_filtered_5))
print("Muestras filtradas N=15:", len(altitude_filtered_15))

print("Altitud original:", altitude[50])
print("Altitud filtrada N=5:", round(altitude_filtered_5[50], 3))
print("Altitud filtrada N=15:", round(altitude_filtered_15[50], 3))

# ==========================================
# CALCULO DE VELOCIDAD VERTICAL
# ==========================================

def calculate_vertical_velocity(altitude_data, time_data):

    velocity = [0.0]

    for i in range(1, len(altitude_data)):

        delta_altitude = (
            altitude_data[i] - altitude_data[i - 1]
        )

        delta_time = (
            time_data[i] - time_data[i - 1]
        ) / 1000

        if delta_time > 0:
            vertical_speed = delta_altitude / delta_time
        else:
            vertical_speed = 0.0

        velocity.append(vertical_speed)

    return velocity


# Calcular velocidades verticales

vertical_velocity_raw = calculate_vertical_velocity(
    altitude, time_ms
)

vertical_velocity_5 = calculate_vertical_velocity(
    altitude_filtered_5, time_ms
)

vertical_velocity_15 = calculate_vertical_velocity(
    altitude_filtered_15, time_ms
)


# ==========================================
# RESUMEN DE VELOCIDADES
# ==========================================

print("\nVELOCIDADES VERTICALES")
print("--------------------------------")

print("Velocidades originales:", len(vertical_velocity_raw))
print("Velocidades N=5:", len(vertical_velocity_5))
print("Velocidades N=15:", len(vertical_velocity_15))

print("Velocidad original:", round(vertical_velocity_raw[50], 3), "m/s")
print("Velocidad N=5:", round(vertical_velocity_5[50], 3), "m/s")
print("Velocidad N=15:", round(vertical_velocity_15[50], 3), "m/s")

# ==========================================
# DETECCION DE EVENTOS DEL VUELO
# ==========================================

# DETECCION DE DESPEGUE

takeoff_index = None

for i in range(len(accel_z)):

    if accel_z[i] > 20.0:
        takeoff_index = i
        break


# DETECCION DE APOGEO

apogee_index = 0

for i in range(1, len(altitude_filtered_15)):

    if altitude_filtered_15[i] > altitude_filtered_15[apogee_index]:
        apogee_index = i


# DETECCION DE ATERRIZAJE

landing_index = None

for i in range(apogee_index + 1, len(altitude)):

    if (
        altitude_filtered_15[i] <= 2.0
        and abs(vertical_velocity_15[i]) <= 1.0
    ):

        if (
            i + 2 < len(altitude)
            and altitude_filtered_15[i + 1] <= 2.0
            and abs(vertical_velocity_15[i + 1]) <= 1.0
            and altitude_filtered_15[i + 2] <= 2.0
            and abs(vertical_velocity_15[i + 2]) <= 1.0
        ):

            landing_index = i
            break


# ==========================================
# RESUMEN DE EVENTOS
# ==========================================

print("\nEVENTOS DEL VUELO")
print("--------------------------------")

if takeoff_index is not None:
    print("Despegue:", time_ms[takeoff_index] / 1000, "s")
else:
    print("Despegue: No detectado")

print("Apogeo:", time_ms[apogee_index] / 1000, "s")
print(
    "Altitud maxima:",
    round(altitude_filtered_15[apogee_index], 3),
    "m"
)

if landing_index is not None:
    print("Aterrizaje:", time_ms[landing_index] / 1000, "s")
else:
    print("Aterrizaje: No detectado")

