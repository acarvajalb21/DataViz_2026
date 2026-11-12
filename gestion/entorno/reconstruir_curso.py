"""Reconstruye los entornos trasladados a partir de sus paquetes registrados."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "gestion" / "entorno"
WORK = ROOT / ".dataviz-runtime" / "configuracion"
WORK.mkdir(parents=True, exist_ok=True)
BACKUP = WORK / "entornos_anteriores"
BACKUP.mkdir(exist_ok=True)
ITEMS = [
    ("curso_dash", "curso/DASH/.venv", "Python313"),
    ("curso_credito", "curso/SEMANA_11/app_dash/.venv", "Python311"),
    ("curso_libro", "curso/jbook_dataviz_2026/.venv", "Python311"),
]


def recreate(item):
    name, relative, version = item
    target = (ROOT / relative).resolve()
    backup = (BACKUP / name).resolve()
    if not target.is_relative_to(ROOT / "curso") or target.name != ".venv":
        raise ValueError(target)
    if not backup.is_relative_to(BACKUP) or backup == BACKUP:
        raise ValueError(backup)
    base = Path(os.environ["LOCALAPPDATA"]) / "Programs" / "Python" / version / "python.exe"
    if backup.exists():
        raise RuntimeError("Ya existe un respaldo pendiente: " + str(backup))
    if not target.exists() or not base.is_file():
        raise FileNotFoundError(str(target) + " / " + str(base))
    shutil.move(str(target), str(backup))
    env = os.environ.copy()
    env.update(PIP_CACHE_DIR=str(ROOT / ".dataviz-runtime/pip-cache"),
               PIP_DISABLE_PIP_VERSION_CHECK="1", PYTHONIOENCODING="utf-8")
    logpath = WORK / (name + ".log")
    with logpath.open("w", encoding="utf-8") as log:
        subprocess.run([str(base), "-m", "venv", str(target)], check=True,
                       stdout=log, stderr=subprocess.STDOUT, env=env)
        python = target / "Scripts/python.exe"
        subprocess.run([str(python), "-m", "pip", "install", "-r", str(REPORT / (name + ".requirements.txt"))],
                       check=True, stdout=log, stderr=subprocess.STDOUT, env=env)
        subprocess.run([str(python), "-m", "pip", "check"], check=True,
                       stdout=log, stderr=subprocess.STDOUT, env=env)
    pip = subprocess.check_output([str(target / "Scripts/pip.exe"), "--version"], text=True).strip()
    book = None
    if name == "curso_libro":
        book = subprocess.check_output([str(target / "Scripts/jupyter-book.exe"), "--version"], text=True).strip()
    # El respaldo contiene únicamente una instalación reproducible, ya reconstruida.
    if backup.parent != BACKUP or not backup.is_relative_to(ROOT / ".dataviz-runtime"):
        raise RuntimeError("Ruta de limpieza inesperada")
    shutil.rmtree(backup)
    result = {"nombre": name, "ruta": relative, "pip_ejecutable": pip,
              "jupyter_book_ejecutable": book, "pip_check": "correcto"}
    print(name + ": reconstruido y verificado", flush=True)
    return result


if __name__ == "__main__":
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(recreate, item) for item in ITEMS]):
            results.append(future.result())
    (REPORT / "entornos_curso.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
