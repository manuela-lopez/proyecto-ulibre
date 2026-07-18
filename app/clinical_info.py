import csv
import unicodedata
from pathlib import Path


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.lower().strip().split())


def load_clinical_info(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}

    info: dict[str, dict[str, str]] = {}
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = normalize_text(row.get("nombre_medicamento"))
            active = normalize_text(row.get("principio_activo"))
            payload = {
                "para_que_sirve": row.get("para_que_sirve", "").strip(),
                "efectos_secundarios": row.get("efectos_secundarios", "").strip(),
            }
            if name:
                info[name] = payload
            if active:
                info[active] = payload
    return info
