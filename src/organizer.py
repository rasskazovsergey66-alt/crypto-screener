# src/organizer.py
"""Сортировка CSV: свежий остаётся в корне, остальные → history/."""

import re
import shutil
from pathlib import Path
from typing import Optional

from config import BASE_DIR, HISTORY_DIR


TIMESTAMP_RE = re.compile(r'(\d{8}_\d{6})')


def _sort_key(path: Path) -> str:
    """Сортировка по timestamp в имени, иначе по mtime."""
    m = TIMESTAMP_RE.search(path.stem)
    if m:
        return m.group(1)
    return f"{path.stat().st_mtime:020.6f}"


def _unique_target(folder: Path, filename: str) -> Path:
    """Путь без конфликтов: если файл есть — добавляет _1, _2, ..."""
    target = folder / filename
    if not target.exists():
        return target
    stem, suffix = target.stem, target.suffix
    i = 1
    while True:
        candidate = folder / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1


def organize_csv_files(verbose: bool = True) -> Optional[Path]:
    """
    Оставляет в корне ТОЛЬКО самый свежий CSV.
    Все остальные CSV из корня → в history/.

    Возвращает путь к оставшемуся свежему файлу (или None).
    """
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    root_csvs = [p for p in BASE_DIR.glob("*.csv") if p.is_file()]

    if verbose:
        print("=" * 60)
        print("🧹 ОРГАНИЗАЦИЯ CSV-ФАЙЛОВ")
        print("=" * 60)

    if not root_csvs:
        if verbose:
            print("ℹ️  CSV-файлы в корне не найдены")
        return None

    if len(root_csvs) == 1:
        if verbose:
            print(f"ℹ️  В корне только один CSV: {root_csvs[0].name}")
            print("=" * 60)
        return root_csvs[0]

    root_csvs.sort(key=_sort_key)
    newest = root_csvs[-1]
    older = root_csvs[:-1]

    if verbose:
        print(f"🔎 Найдено CSV в корне: {len(root_csvs)}")
        print(f"⭐ Оставляем: {newest.name}")

    for path in older:
        target = _unique_target(HISTORY_DIR, path.name)
        shutil.move(str(path), str(target))
        if verbose:
            print(f"   📦 {path.name} → history/{target.name}")

    if verbose:
        print(f"✅ Готово. В корне остался: {newest.name}")
        print("=" * 60)

    return newest


if __name__ == "__main__":
    organize_csv_files()