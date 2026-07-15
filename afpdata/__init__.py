"""afpdata: descarga y procesamiento de valores cuota y patrimonio de los fondos AFP de Chile.

Los datos provienen de la Superintendencia de Pensiones (spensiones.cl).
"""

__version__ = "1.0.0"

FONDOS = ["A", "B", "C", "D", "E"]

# Año de inicio de cada tipo de fondo (los multifondos A/B/D nacen en 2002,
# el fondo E en 2000 y el fondo C es el histórico desde 1981).
INIT_YEAR = {"A": 2002, "B": 2002, "C": 1981, "D": 2002, "E": 2000}
