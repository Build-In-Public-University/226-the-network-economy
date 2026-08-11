from __future__ import annotations

import argparse
from pathlib import Path

from .analyze import write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Map claims and arguments in a source document.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, default=Path("data"))
    args = parser.parse_args()
    write_outputs(args.source, args.out)
    print(f"wrote analysis to {args.out.resolve()}")


if __name__ == "__main__":
    main()
