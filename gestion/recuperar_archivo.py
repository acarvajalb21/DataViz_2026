"""Recupera un archivo anterior usando el índice de migración, sin sobrescribir."""
from pathlib import Path, PurePosixPath
import argparse
import csv
import hashlib
import io
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "RESPALDO_DATAVIZ_MIGRACION/"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ruta_anterior", help="Ruta exacta del índice CSV")
    parser.add_argument("--destino", type=Path, default=ROOT / "archivo" / "recuperados")
    args = parser.parse_args()
    relative = PurePosixPath(args.ruta_anterior.replace("\\", "/"))
    if relative.is_absolute() or ".." in relative.parts or ":" in str(relative):
        parser.error("Ruta anterior no válida")
    with (ROOT / "gestion/migracion/recuperacion_versiones_anteriores.csv").open(encoding="utf-8-sig",newline="") as stream:
        row = next((r for r in csv.DictReader(stream) if r["ruta_anterior"] == str(relative)), None)
    if row is None:
        parser.error("No existe esa ruta en el índice")
    location = row["recuperar_desde"].split("!/")
    with zipfile.ZipFile(ROOT / "archivo" / location[0]) as archive:
        member = location[1]
        if location[0] == "RESPALDO_DATAVIZ_MIGRACION.zip":
            member = PREFIX + member
        data = archive.read(member)
    if len(location) == 3:
        with zipfile.ZipFile(io.BytesIO(data)) as nested:
            data = nested.read(location[2])
    if hashlib.sha256(data).hexdigest() != row["sha256"]:
        raise RuntimeError("La huella del archivo no coincide; no se escribe")
    target = args.destino.resolve().joinpath(*relative.parts)
    if target.exists():
        raise FileExistsError(f"El destino ya existe: {target}")
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    print(target)


if __name__ == "__main__":
    main()
