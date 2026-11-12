"""Descarga versiones oficiales verificadas para preparar este computador."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / ".dataviz-runtime" / "descargas"
DEST.mkdir(parents=True, exist_ok=True)
FILES = [
    ("python-3.12.10-amd64.exe", "https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe",
     "md5", "5eddb0b6f12c852725de071ae681dde4"),
    ("google-cloud-sdk-593.0.0.zip", "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-593.0.0-windows-x86_64-bundled-python.zip",
     "sha256", "8fbdc9d644ffdd25a7f515c2643edc87100d3d48be9d3aa635454f6d7fb6a53c"),
]


def download(item):
    name, url, algorithm, expected = item
    path = DEST / name
    if not path.exists():
        urllib.request.urlretrieve(url, path)
    fingerprint = hashlib.file_digest(path.open("rb"), algorithm).hexdigest()
    if fingerprint != expected:
        raise RuntimeError("Huella inesperada: " + name)
    print(name, path.stat().st_size, algorithm, "verificado", flush=True)


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(download, FILES))
