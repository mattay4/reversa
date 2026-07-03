#!/usr/bin/env python3
"""
extract_deps.py — Produz deps.json para o Time Reversa Docs.

Esqueleto da Onda 1. Análise real de imports por linguagem entra na TASK-07.

Schema de saída: ver specs/reversa-docs/design.md, seção "Schema de deps.json".

Uso:
    python extract_deps.py --modules _reversa_docs/assets/data/modules.json \
                           --out _reversa_docs/assets/data/deps.json
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modules", required=True,
                        help="Caminho para modules.json gerado por extract_modules.py")
    parser.add_argument("--out", required=True, help="Caminho de saída do deps.json")
    args = parser.parse_args()

    modules_data = json.loads(Path(args.modules).read_text(encoding="utf-8"))
    nodes = [{"id": m["id"]} for m in modules_data.get("modules", [])]

    # Análise de imports real na TASK-07. Por ora apenas nodes vazios + edges vazias.
    out = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "nodes": nodes,
        "edges": [],
        "cycles": [],
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK (esqueleto): {len(nodes)} nodes, 0 edges em {out_path}")


if __name__ == "__main__":
    main()
