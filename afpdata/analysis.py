"""Genera los gráficos de análisis por AFP.

Reemplaza a los antiguos notebooks ``ValoresCuota<AFP>.ipynb`` (y a
``copynb.py`` que los replicaba). Produce, por cada AFP, los mismos cuatro
gráficos que calculaban los notebooks:

* valor cuota multifondos (histórico completo)
* rentabilidad anualizada (suma de rentabilidades mensuales)
* rentabilidad semanal de los últimos 365 días
* valor cuota y rentabilidad diaria de los últimos 60 días

Uso::

    python -m afpdata.analysis                # todas las AFP vigentes
    python -m afpdata.analysis CUPRUM UNO     # solo algunas
"""

from __future__ import annotations

import argparse
import os
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

# AFP vigentes (con archivo VC-*.csv actualizado a la fecha).
AFPS_VIGENTES = [
    "CAPITAL",
    "CUPRUM",
    "HABITAT",
    "MODELO",
    "PLANVITAL",
    "PROVIDA",
    "UNO",
]

# Fondos a graficar (extremos y el histórico C, como en los notebooks).
FONDOS_PLOT = ["A", "C", "E"]

FIGSIZE = (15, 5)


def _log(msg: str) -> None:
    print(f"[afpdata.analysis] {msg}", file=sys.stderr, flush=True)


def load_afp(afp: str, data_dir: str = "data") -> pd.DataFrame:
    """Lee data/VC-<AFP>.csv con el formato chileno del proyecto."""
    path = os.path.join(data_dir, f"VC-{afp}.csv")
    return pd.read_csv(
        path, sep=";", decimal=",", index_col=0, parse_dates=True
    )


def _fondos(df: pd.DataFrame) -> list[str]:
    return [f for f in FONDOS_PLOT if f in df.columns]


def _save(fig, out_dir: str, name: str, written: list[str]) -> None:
    path = os.path.join(out_dir, name)
    fig.savefig(path, dpi=100, bbox_inches="tight")
    plt.close(fig)
    written.append(path)


def charts_afp(afp: str, data_dir: str = "data", out_dir: str = "charts") -> list[str]:
    """Genera los cuatro gráficos de una AFP y devuelve las rutas escritas."""
    os.makedirs(out_dir, exist_ok=True)
    written: list[str] = []

    df = load_afp(afp, data_dir)[lambda d: _fondos(d)].dropna(how="all")

    # 1. Valor cuota multifondos, histórico completo.
    ax = df.plot(title=f"Multifondos {afp}", figsize=FIGSIZE)
    ax.set_ylabel("Valor cuota [$]")
    _save(ax.get_figure(), out_dir, f"{afp}_multifondos.png", written)

    # 2. Rentabilidad anualizada: suma de rentabilidades mensuales por año
    #    (misma aproximación que usaban los notebooks).
    mensual = df.dropna().resample("MS").first().pct_change()
    anual = mensual.resample("YE").sum()
    anual.index = anual.index.year
    ax = anual.plot(kind="bar", title=f"Rentabilidad anualizada {afp}", figsize=FIGSIZE)
    ax.yaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    ax.set_xlabel("Año")
    _save(ax.get_figure(), out_dir, f"{afp}_rentabilidad_anual.png", written)

    # 3. Rentabilidad semanal, últimos 365 días.
    ult_365 = df.loc[df.index.max() - pd.Timedelta(days=365) :]
    semanal = ult_365.resample("W").first().pct_change()
    ax = semanal.plot(
        title=f"Rentabilidad semanal últimos 365 días {afp}", figsize=FIGSIZE
    )
    ax.yaxis.set_major_formatter(lambda x, _: f"{x:.1%}")
    _save(ax.get_figure(), out_dir, f"{afp}_rentabilidad_semanal.png", written)

    # 4. Valor cuota y rentabilidad diaria, últimos 60 días con datos.
    ult_60 = df.dropna(how="all").iloc[-60:]
    ax = ult_60.plot(title=f"Valor cuota últimos 60 días {afp}", figsize=FIGSIZE)
    ax.set_ylabel("Valor cuota [$]")
    _save(ax.get_figure(), out_dir, f"{afp}_valor_cuota_60d.png", written)

    ax = ult_60.pct_change().plot(
        title=f"Rentabilidad diaria últimos 60 días {afp}", figsize=FIGSIZE
    )
    ax.yaxis.set_major_formatter(lambda x, _: f"{x:.2%}")
    _save(ax.get_figure(), out_dir, f"{afp}_rentabilidad_diaria_60d.png", written)

    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="afpdata.analysis",
        description="Genera gráficos de análisis por AFP a partir de data/.",
    )
    parser.add_argument(
        "afps",
        nargs="*",
        default=AFPS_VIGENTES,
        help=f"AFP a graficar (por defecto: {' '.join(AFPS_VIGENTES)})",
    )
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--out-dir", default="charts")
    args = parser.parse_args(argv)

    for afp in args.afps:
        written = charts_afp(afp.upper(), data_dir=args.data_dir, out_dir=args.out_dir)
        _log(f"{afp}: {len(written)} gráficos")
    _log(f"listo → {args.out_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
