"""Comprueba los iniciadores y cierra todos los procesos que crea la prueba."""
from pathlib import Path
import json
import os
import shutil
import socket
import subprocess
import time
import urllib.request

import psutil

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / ".dataviz-runtime/configuracion"
SHELL = shutil.which("pwsh") or str(Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe")


def busy(port):
    with socket.socket() as sock:
        sock.settimeout(1)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def smoke(name, port, routes):
    if busy(port):
        raise RuntimeError(f"El puerto {port} ya estaba ocupado; no se interrumpe ese proceso")
    statuses = {}
    created = time.time()
    log = (WORK / ("servidor_" + name.lower() + ".log")).open("w",encoding="utf-8")
    proc = subprocess.Popen([SHELL,"-NoProfile","-File",str(ROOT / "ABRIR_DATAVIZ.ps1"),name,"-SinNavegador"],
                            cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name=="nt" else 0)
    try:
        deadline = time.monotonic() + 60
        while not busy(port):
            if proc.poll() is not None:
                raise RuntimeError(f"{name} terminó antes de iniciar; revisar su log")
            if time.monotonic() > deadline:
                raise TimeoutError(name)
            time.sleep(.25)
        for route in routes:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}{route}",timeout=15) as response:
                statuses[route] = response.status
                if response.status != 200:
                    raise RuntimeError((name,route,response.status))
    finally:
        # Se identifican tanto los hijos como el dueño real del puerto. No se usa un PID antiguo.
        owned = {}
        try:
            parent = psutil.Process(proc.pid)
            owned.update({p.pid:p for p in parent.children(recursive=True)})
            owned[parent.pid] = parent
        except psutil.NoSuchProcess:
            pass
        for connection in psutil.net_connections(kind="tcp"):
            if connection.status==psutil.CONN_LISTEN and connection.laddr.port==port and connection.pid:
                candidate=psutil.Process(connection.pid)
                command=" ".join(candidate.cmdline()).lower()
                if candidate.create_time() >= created-1 and ("proyecto_salud/shiny_salud" in command or "dash_salud.app" in command or "http.server" in command):
                    owned[candidate.pid]=candidate
        for process in owned.values():
            try:process.kill()
            except psutil.NoSuchProcess:pass
        psutil.wait_procs(list(owned.values()),timeout=10)
        log.close()
        deadline=time.monotonic()+8
        while busy(port) and time.monotonic()<deadline:
            time.sleep(.25)
        if busy(port):
            raise RuntimeError(f"La limpieza de {name} no liberó el puerto {port}")
    print(name + ": HTTP 200; puerto libre después de la prueba",flush=True)
    return {"http":statuses,"puerto":port,"libre_despues":True}


if __name__=="__main__":
    result={"shiny":smoke("Shiny",3838,["/"]),
            "dash":smoke("Dash",8050,["/","/health","/_dash-layout","/informe/","/api/asistente/estado"]),
            "bookdown":smoke("Bookdown",4321,["/","/index.html"]),
            "jupyter_book":smoke("JupyterBook",4322,["/","/intro.html"])}
    (ROOT / "gestion/entorno/servidores.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
