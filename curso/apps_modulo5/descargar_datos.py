"""Descarga únicamente los CSV utilizados por las tres aplicaciones finales."""

from urllib.request import urlopen

from comun import DATA

FUENTES = {
    "data_banco_creditos.csv": "https://raw.githubusercontent.com/cdeoroaguado/Datos/refs/heads/main/datadescrip/data_banco_creditos.csv",
    "intro_bees.csv": "https://raw.githubusercontent.com/cdeoroaguado/Datos/refs/heads/main/dataviz/intro_bees.csv",
    "dash-stock-ticker-demo.csv": "https://raw.githubusercontent.com/cdeoroaguado/Datos/refs/heads/main/dataviz/dash-stock-ticker-demo.csv",
}


def descargar():
    DATA.mkdir(parents=True, exist_ok=True)
    for nombre, url in FUENTES.items():
        with urlopen(url, timeout=60) as respuesta:
            contenido = respuesta.read()
        destino = DATA / nombre
        destino.write_bytes(contenido)
        print(f"Guardado: {nombre} ({len(contenido):,} bytes)")


if __name__ == "__main__":
    descargar()
