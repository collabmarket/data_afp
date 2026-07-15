"""Parseo del CSV crudo de la Superintendencia a un DataFrame ordenado.

El CSV crudo viene en bloques separados por líneas en blanco. Cada bloque
corresponde a un período con un conjunto estable de AFP y tiene la forma::

    Valores Confirmados
    <línea en blanco>
    Fecha;ALAMEDA;;CONCORDIA;;CUPRUM;;...
    ;Valor Cuota;Valor Patrimonio;Valor Cuota;Valor Patrimonio;...
    1981-06-01;100,0;0,0;;;100,0;0,0;...
    ...

Esta lógica reemplaza a ``cleancsv.py`` (que dividía en archivos temporales)
y a la parte de lectura de ``curator.py``.
"""

from __future__ import annotations

import io

import pandas as pd


def _iter_blocks(text: str) -> list[list[str]]:
    """Divide el texto en bloques usando las líneas en blanco como separador."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in normalized.split("\n"):
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line)
    if current:
        blocks.append(current)
    return blocks


def _parse_block(block: list[str]) -> pd.DataFrame:
    """Convierte un bloque (encabezado AFP + encabezado ítem + datos) en DataFrame."""
    afp_tokens = block[0].split(";")
    item_tokens = block[1].split(";")

    # El encabezado de ítems tiene exactamente 2 columnas por AFP y es la
    # fuente confiable para la cantidad de columnas de valores.
    value_count = len(item_tokens) - 1

    # Nombres de AFP: aparecen en la primera de cada par de columnas y se
    # repiten hacia adelante. La última AFP del encabezado a veces no trae el
    # ";;" de relleno, así que se completa con vacíos hasta value_count.
    afp_values = [t.strip() for t in afp_tokens[1:]]
    afp_values += [""] * (value_count - len(afp_values))

    afps: list[str] = []
    last: str | None = None
    for token in afp_values:
        if token:
            last = token
        afps.append(last or "")

    items = [t.strip() for t in item_tokens[1:]]
    columns = pd.MultiIndex.from_arrays([afps, items], names=["AFP", "Item"])

    data = pd.read_csv(
        io.StringIO("\n".join(block[2:])),
        sep=";",
        header=None,
        decimal=",",
        thousands=".",
    )
    dates = pd.to_datetime(data.iloc[:, 0], format="%Y-%m-%d")
    values = data.iloc[:, 1 : value_count + 1].copy()
    values.columns = columns
    values.index = pd.Index(dates, name="Fecha")
    return values


def parse_raw(text: str) -> pd.DataFrame:
    """Parsea el CSV crudo de un tipo de fondo.

    Devuelve un DataFrame con índice ``Fecha`` (datetime) y columnas
    MultiIndex ``(AFP, Item)`` donde *Item* es "Valor Cuota" o
    "Valor Patrimonio".
    """
    frames = [
        _parse_block(block)
        for block in _iter_blocks(text)
        if block and block[0].startswith("Fecha;")
    ]
    if not frames:
        raise ValueError("No se encontraron bloques de datos en el CSV crudo")

    df = pd.concat(frames)
    df.columns.names = ["AFP", "Item"]
    df.index.name = "Fecha"
    # Ante fechas repetidas en los límites de bloque, conserva la última.
    df = df[~df.index.duplicated(keep="last")]
    return df.sort_index()
