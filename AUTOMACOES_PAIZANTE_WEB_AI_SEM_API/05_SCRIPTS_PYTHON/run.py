"""Ponto de entrada do menu interativo da central Automacoes Paizante Web AI."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.main_menu import rodar_menu  # noqa: E402

if __name__ == "__main__":
    rodar_menu()
