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
