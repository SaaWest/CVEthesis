from pathlib import Path

def writeFile(dir, files):
    base = Path(dir)

    for file in files:
        path = base / file["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(file["content"])