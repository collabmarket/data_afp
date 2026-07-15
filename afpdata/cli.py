"""Interfaz de línea de comandos: descarga, parsea y genera los CSV.

Uso::

    python -m afpdata                 # descarga en vivo y actualiza data/
    python -m afpdata --raw-dir raw   # además guarda los CSV crudos
    python -m afpdata --from-raw raw  # reprocesa sin descargar (usa raw/)
"""

from __future__ import annotations

import argparse
import os
import sys

import requests

from . import FONDOS
from .build import build_all
from .parse import parse_raw
from .source import ENCODING, download_fondo


def _log(msg: str) -> None:
    print(f"[afpdata] {msg}", file=sys.stderr, flush=True)


def _load_data(args) -> dict:
    data = {}
    session = requests.Session()
    for fondo in FONDOS:
        if args.from_raw:
            path = os.path.join(args.from_raw, f"vcf{fondo}.csv")
            _log(f"leyendo crudo {path}")
            with open(path, encoding=ENCODING) as fh:
                text = fh.read()
        else:
            _log(f"descargando fondo {fondo} ...")
            text = download_fondo(fondo, session=session)
            if args.raw_dir:
                os.makedirs(args.raw_dir, exist_ok=True)
                raw_path = os.path.join(args.raw_dir, f"vcf{fondo}.csv")
                with open(raw_path, "w", encoding=ENCODING) as fh:
                    fh.write(text)
                _log(f"crudo guardado en {raw_path}")
        df = parse_raw(text)
        _log(
            f"fondo {fondo}: {len(df)} filas, "
            f"{df.index.min().date()} → {df.index.max().date()}"
        )
        data[fondo] = df
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="afpdata",
        description="Descarga y procesa valores cuota/patrimonio de fondos AFP Chile.",
    )
    parser.add_argument(
        "--out-dir", default="data", help="directorio de salida (por defecto: data)"
    )
    parser.add_argument(
        "--raw-dir",
        default=None,
        help="si se indica, guarda los CSV crudos descargados en este directorio",
    )
    parser.add_argument(
        "--from-raw",
        default=None,
        metavar="DIR",
        help="reprocesa desde CSV crudos existentes en DIR, sin descargar",
    )
    args = parser.parse_args(argv)

    data = _load_data(args)
    written = build_all(data, outdir=args.out_dir)
    _log(f"escritos {len(written)} archivos en {args.out_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
