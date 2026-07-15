"""Descarga de datos crudos desde la Superintendencia de Pensiones.

El sitio genera un CSV directamente vía HTTP GET, por lo que no se necesita
navegador ni Selenium (a diferencia de la versión original en Ruby/webdrone).

Endpoint (descubierto en la función ``generaXLS()`` del formulario web)::

    https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFPxls.php
        ?aaaaini=<año inicio>&aaaafin=<año fin>&tf=<fondo>&fecconf=<YYYYMMDD>
"""

from __future__ import annotations

import datetime as _dt

import requests

from . import INIT_YEAR

BASE_URL = "https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFPxls.php"

# El servidor entrega el CSV en Latin-1 (iso-8859-1).
ENCODING = "iso-8859-1"

DEFAULT_TIMEOUT = 60
DEFAULT_HEADERS = {
    "User-Agent": (
        "afpdata/1.0 (+https://github.com/collabmarket/data_afp) "
        "python-requests"
    )
}


def download_fondo(
    fondo: str,
    *,
    year_from: int | None = None,
    year_to: int | None = None,
    session: requests.Session | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> str:
    """Descarga el CSV crudo de un tipo de fondo y devuelve su texto.

    Por defecto descarga todo el histórico disponible (desde el año de inicio
    del fondo hasta el año en curso).
    """
    fondo = fondo.upper()
    if fondo not in INIT_YEAR:
        raise ValueError(f"Fondo desconocido: {fondo!r} (esperado A-E)")

    today = _dt.date.today()
    year_from = year_from if year_from is not None else INIT_YEAR[fondo]
    year_to = year_to if year_to is not None else today.year

    params = {
        "aaaaini": year_from,
        "aaaafin": year_to,
        "tf": fondo,
        "fecconf": today.strftime("%Y%m%d"),
    }

    http = session or requests
    resp = http.get(
        BASE_URL, params=params, headers=DEFAULT_HEADERS, timeout=timeout
    )
    resp.raise_for_status()
    resp.encoding = ENCODING
    text = resp.text
    if "Fecha" not in text:
        raise RuntimeError(
            f"Respuesta inesperada para fondo {fondo}: no contiene datos "
            f"(¿cambió el endpoint {BASE_URL}?)"
        )
    return text
