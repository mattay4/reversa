#!/usr/bin/env python3
"""
convert_chronicle.py — Converte .reversa/chronicle.md em timeline.json.

Esqueleto da Onda 1. Parser real de markdown e classificação de eventos na TASK-09.

Uso:
    python convert_chronicle.py --src .reversa/chronicle.md \
                                --out _reversa_docs/assets/data/timeline.json
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

DATE_PATTERN = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
HEADING_PATTERN = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)


def parse_chronicle(text: str):
    events = []
    for line in text.splitlines():
        date_match = DATE_PATTERN.search(line)
        if not date_match:
            continue
        events.append({
            "date": date_match.group(1),
            "title": line.strip("-* ").strip()[:120],
            "raw": line.strip(),
        })
    return events


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", required=True, help="Caminho para .reversa/chronicle.md")
    parser.add_argument("--out", required=True, help="Caminho de saída do timeline.json")
    args = parser.parse_args()

    src = Path(args.src)
    if not src.exists():
        print(f"AVISO: {src} não existe. Pulando geração de timeline.json.")
        return

    text = src.read_text(encoding="utf-8")
    events = parse_chronicle(text)

    out = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "events": events,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(events)} eventos em {out_path}")


if __name__ == "__main__":
    main()
