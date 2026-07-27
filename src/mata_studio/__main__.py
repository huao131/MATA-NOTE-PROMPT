from __future__ import annotations

import argparse
import os

from .api import serve
from .app import StudioApp


def main() -> None:
    parser = argparse.ArgumentParser(description="MATA AI VIDEO STUDIO")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--data-dir", default=os.getenv("MATA_STUDIO_DATA_DIR", ".local/mata-studio"))
    args = parser.parse_args()
    serve(StudioApp(args.data_dir), args.host, args.port)


if __name__ == "__main__":
    main()
