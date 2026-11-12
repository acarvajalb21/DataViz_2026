"""Crea entornos separados para modelo, libro y aplicación Dash."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "gestion/entorno"
WORK = ROOT / ".dataviz-runtime/configuracion"
WORK.mkdir(parents=True, exist_ok=True)
BASE = Path(os.environ["LOCALAPPDATA"]) / "Programs/Python/Python312/python.exe"
ITEMS = [
    ("modelo_salud", "proyecto_salud/ml_salud", REPORT / "modelo_notebook.requirements.txt", "modelo-salud", "Modelo Salud · Python 3.12 · pandas 3"),
    ("libro_salud", "proyecto_salud/jupyter_salud", ROOT / "proyecto_salud/jupyter_salud/requirements.txt", "libro-salud", "Libro Salud · Python 3.12 · pandas 2"),
    ("dash_salud", "proyecto_salud/dash_salud", ROOT / "proyecto_salud/dash_salud/requirements.txt", None, None),
    ("apps_modulo5", "curso/apps_modulo5", ROOT / "curso/apps_modulo5/requirements.txt", None, None),
]


def install(item):
    name, directory, requirements, kernel, display = item
    target = (ROOT / directory / ".venv").resolve()
    if not any(target.is_relative_to(ROOT / area) for area in ["proyecto_salud","curso"]) or target.name != ".venv":
        raise ValueError(target)
    env = os.environ.copy()
    env.update(PIP_CACHE_DIR=str(ROOT / ".dataviz-runtime/pip-cache"),
               PIP_DISABLE_PIP_VERSION_CHECK="1", PYTHONIOENCODING="utf-8")
    python = target / "Scripts/python.exe"
    print(name + ": preparando", flush=True)
    with (WORK / (name + ".log")).open("w",encoding="utf-8") as log:
        if not python.is_file():
            subprocess.run([str(BASE), "-m", "venv", str(target)], check=True, env=env,
                           stdout=log, stderr=subprocess.STDOUT)
        subprocess.run([str(python), "-m", "pip", "install", "-r", str(requirements)], check=True,
                       env=env, stdout=log, stderr=subprocess.STDOUT)
        subprocess.run([str(python), "-m", "pip", "check"], check=True, env=env,
                       stdout=log, stderr=subprocess.STDOUT)
        if kernel:
            subprocess.run([str(python), "-m", "ipykernel", "install", "--prefix", str(ROOT / ".venv"),
                            "--name", kernel, "--display-name", display], check=True,
                           env=env, stdout=log, stderr=subprocess.STDOUT)
            spec = ROOT / ".venv/share/jupyter/kernels" / kernel / "kernel.json"
            metadata = json.loads(spec.read_text(encoding="utf-8"))
            metadata["env"] = {"CNPV_DATOS": str(ROOT / "proyecto_salud/datos"),
                               "PYTHONPATH": str(ROOT / "proyecto_salud")}
            chrome = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
            if chrome.is_file(): metadata["env"]["BROWSER_PATH"] = str(chrome)
            spec.write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding="utf-8")
    freeze = subprocess.check_output([str(python), "-m", "pip", "freeze", "--all"], text=True)
    (REPORT / (name + ".freeze.txt")).write_text(freeze,encoding="utf-8")
    packages = json.loads(subprocess.check_output([str(python), "-m", "pip", "list", "--format=json"],text=True))
    package_versions = {p["name"].lower():p["version"] for p in packages}
    result = {"nombre":name,"python":str(python),"version_python":subprocess.check_output([str(python),"--version"],text=True).strip(),
              "paquetes":package_versions,"pip_check":"correcto","kernel":kernel}
    print(name + ": instalado y verificado",flush=True)
    return result


if __name__ == "__main__":
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(install,item) for item in ITEMS]):
            results.append(future.result())
    (REPORT / "entornos_salud.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
