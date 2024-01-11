import pandas as pd

# Leer el archivo "registros_ventas.txt" línea por línea
with open("registros_ventas.txt", "r") as file:
    lines = file.readlines()

# Procesar las líneas y producir una lista de diccionarios
data = []
current_record = {}
for line in lines:
    if line.strip():  # Ignorar líneas en blanco
        key, value = line.strip().split(": ")
        current_record[key] = value
    else:
        data.append(current_record)
        current_record = {}

# Crear un DataFrame de pandas con los datos extraídos
df = pd.DataFrame(data)

# Aplicar técnicas de limpieza de datos en el DataFrame
# Convertir Cantidad y Precio a números
df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce")
df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce")

# Reemplazar los valores faltantes en Cantidad y Precio por la media de la columna
df["Cantidad"].fillna(df["Cantidad"].mean(), inplace=True)
df["Precio"].fillna(df["Precio"].mean(), inplace=True)

# Eliminar outliers en Cantidad y Precio usando el rango intercuartil
Q1 = df["Cantidad"].quantile(0.25)
Q3 = df["Cantidad"].quantile(0.75)
IQR = Q3 - Q1
df = df[(df["Cantidad"] >= Q1 - 1.5 * IQR) & (df["Cantidad"] <= Q3 + 1.5 * IQR)]

Q1 = df["Precio"].quantile(0.25)
Q3 = df["Precio"].quantile(0.75)
IQR = Q3 - Q1
df = df[(df["Precio"] >= Q1 - 1.5 * IQR) & (df["Precio"] <= Q3 + 1.5 * IQR)]

# Guardar el DataFrame limpio en un nuevo archivo "registros_ventas_limpios.csv"
df.to_csv("registros_ventas_limpios.csv", index=False)
