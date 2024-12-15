# my_module/__init__.py

import sys
from pathlib import Path
import shutil
import gitignore_parser

def copy_directory_with_gitignore(src_dir, dst_dir, gitignore_path=".gitignore"):
    """
    Kopiert ein Verzeichnis, wobei die Regeln eines .gitignore-Files beachtet werden.
    """
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)

    gitignore_path = src_dir / gitignore_path
    if gitignore_path.exists():
        matcher = gitignore_parser.parse_gitignore(gitignore_path)
    else:
        raise FileNotFoundError(f"Die .gitignore-Datei wurde nicht gefunden: {gitignore_path}")

    for src_path in src_dir.rglob("*"):
        rel_path = src_path.relative_to(src_dir)
        dst_path = dst_dir / rel_path

        if matcher(src_path):
            print(f"Ignoriere: {src_path}")
            continue

        if src_path.is_file():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)
            print(f"Kopiert: {src_path} -> {dst_path}")

        elif src_path.is_dir():
            dst_path.mkdir(parents=True, exist_ok=True)
            print(f"Erstelle Verzeichnis: {dst_path}")

# Hauptprogramm, falls das Modul direkt ausgeführt wird
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Verwendung: python -m my_module <source_directory> <destination_directory>")
        sys.exit(1)

    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]

    copy_directory_with_gitignore(src_dir, dst_dir)