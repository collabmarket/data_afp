"""Genera los CSV de salida a partir de los DataFrames por fondo.

Reemplaza a ``curator.py``. Para cada tipo de fondo (A-E) produce:

* ``data/f{X}.csv``      – valor cuota y patrimonio, un fondo, todas las AFP.
* ``data/vcf{X}.csv``    – valor cuota, un fondo, todas las AFP.
* ``data/patf{X}.csv``   – valor patrimonio, un fondo, todas las AFP.

Y para cada AFP:

* ``data/VC-{AFP}.csv``  – valor cuota, una AFP, todos los fondos.
* ``data/PAT-{AFP}.csv`` – valor patrimonio, una AFP, todos los fondos.

Mejora respecto de la versión original: el patrimonio se escribe como entero
(antes algunas celdas salían en notación científica, p.ej. ``8,62226842748e+12``).
"""

from __future__ import annotations

import os
from collections.abc import Mapping

import pandas as pd

from . import FONDOS

VALOR_CUOTA = "Valor Cuota"
VALOR_PATRIMONIO = "Valor Patrimonio"


def _fmt(value: float, item: str) -> str:
    """Formatea un valor al estilo chileno (coma decimal) para el CSV."""
    if pd.isna(value):
        return ""
    if item == VALOR_PATRIMONIO:
        # Pesos: entero, sin notación científica ni separador de miles.
        return str(int(round(value)))
    # Valor cuota: representación decimal más corta que redondea de vuelta.
    return repr(float(value)).replace(".", ",")


def _format_columns(df: pd.DataFrame, item_of) -> pd.DataFrame:
    """Devuelve una copia del DataFrame con cada columna formateada a texto."""
    out = pd.DataFrame(index=df.index)
    for col in df.columns:
        item = item_of(col)
        out[col] = [_fmt(v, item) for v in df[col]]
    out.columns = df.columns
    out.index.name = df.index.name
    return out


def _write(df: pd.DataFrame, path: str, item_of) -> None:
    _format_columns(df, item_of).to_csv(path, sep=";")


def build_all(data: Mapping[str, pd.DataFrame], outdir: str = "data") -> list[str]:
    """Escribe todos los CSV de salida y devuelve la lista de rutas escritas."""
    os.makedirs(outdir, exist_ok=True)
    written: list[str] = []

    def _save(df, name, item_of):
        path = os.path.join(outdir, name)
        _write(df, path, item_of)
        written.append(path)

    # --- Archivos por fondo -------------------------------------------------
    for letra in FONDOS:
        df = data[letra]

        # f{X}: todas las AFP, valor cuota y patrimonio (columnas MultiIndex).
        _save(df, f"f{letra}.csv", item_of=lambda col: col[1])

        # vcf{X} / patf{X}: un item, todas las AFP como columnas.
        for prefix, item in ((("vcf"), VALOR_CUOTA), (("patf"), VALOR_PATRIMONIO)):
            sub = df.xs(item, axis=1, level="Item")
            sub.columns.name = None
            _save(sub, f"{prefix}{letra}.csv", item_of=lambda col, item=item: item)

    # --- Archivos por AFP ---------------------------------------------------
    afps = sorted(
        {afp for df in data.values() for afp in df.columns.get_level_values("AFP")}
    )
    for afp in afps:
        afp_slug = afp.replace(" ", "-")
        for prefix, item in ((("VC"), VALOR_CUOTA), (("PAT"), VALOR_PATRIMONIO)):
            cols = {}
            for letra in FONDOS:
                df = data[letra]
                if (afp, item) in df.columns:
                    cols[letra] = df[(afp, item)]
            if not cols:
                continue
            merged = pd.DataFrame(cols)
            merged.index.name = "Fecha"
            merged = merged.dropna(how="all").sort_index()
            _save(
                merged,
                f"{prefix}-{afp_slug}.csv",
                item_of=lambda col, item=item: item,
            )

    return written
