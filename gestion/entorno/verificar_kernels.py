"""Comprueba los kernels a través del servidor Jupyter y elimina solo los creados aquí."""
from pathlib import Path
import json
import time
import urllib.request
import uuid

import websocket
from jupyter_client.session import Session

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / ".dataviz-runtime/jupyter-runtime"
SERVER = json.loads(next(RUNTIME.glob("jpserver-*.json")).read_text(encoding="utf-8"))


def api(path, method="GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(SERVER["url"] + path, data=data, method=method,
              headers={"Authorization":"token " + SERVER["token"],"Content-Type":"application/json"})
    with urllib.request.urlopen(request,timeout=40) as response:
        content=response.read()
        return json.loads(content) if content else None


def check(name, pandas_major):
    kernel=api("api/kernels","POST",{"name":name,"path":"proyecto_salud/jupyter_salud"})
    client=None
    outputs=[]
    try:
        # Se usa el mismo canal WebSocket que JupyterLab, sin un cliente ZMQ externo.
        session_id=uuid.uuid4().hex
        url=SERVER["url"].replace("http://","ws://",1)+"api/kernels/"+kernel["id"]+"/channels?session_id="+session_id
        client=websocket.create_connection(url,timeout=40,
            header=["Authorization: token "+SERVER["token"]],origin=SERVER["url"].rstrip("/"))
        source="import sys,json,pandas as pd,numpy as np\nfrom pathlib import Path\n"
        if name=="modelo-salud":source+="from ml_salud.contexto import FEATURES_V2\nassert len(FEATURES_V2)==28\n"
        source+=f"assert pd.__version__.split('.')[0]=='{pandas_major}'\n"
        source+="print(json.dumps({'python':sys.version.split()[0],'ejecutable':sys.executable,'pandas':pd.__version__,'numpy':np.__version__,'cwd':str(Path.cwd())}))"
        message=Session().msg("execute_request",content={"code":source,"silent":False,"store_history":False,
                 "user_expressions":{},"allow_stdin":False,"stop_on_error":True})
        message["channel"]="shell"
        message_id=message["header"]["msg_id"]
        client.send(json.dumps(message,default=lambda value:value.isoformat()))
        while True:
            message=json.loads(client.recv())
            if message.get("parent_header",{}).get("msg_id")!=message_id:continue
            kind=message["header"]["msg_type"];content=message["content"]
            if kind=="error":raise RuntimeError(content["ename"] + ": " + content["evalue"])
            if kind=="stream":outputs.append(content["text"])
            if kind=="status" and content["execution_state"]=="idle":break
        result=json.loads("".join(outputs).strip())
        print(name + ": " + result["python"] + ", pandas " + result["pandas"],flush=True)
        return result
    finally:
        if client is not None:client.close()
        api("api/kernels/" + kernel["id"],"DELETE")


if __name__=="__main__":
    specs=api("api/kernelspecs")["kernelspecs"]
    assert all(name in specs for name in ["modelo-salud","libro-salud"])
    targets=[("modelo-salud","3"),("libro-salud","2")]
    if "credito-curso" in specs:targets.append(("credito-curso","2"))
    result={name:check(name,major) for name,major in targets}
    (ROOT / "gestion/entorno/kernels.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
