# utils/helpers.py

from typing import Mapping, Optional, Sequence


def select_record(
    records: Sequence[Mapping[str, object]],
    item_name: str,
) -> Optional[int]:
    if not records:
        print(f"No hay registros de {item_name} disponibles.")
        return None

    print(f"\nSelecciona un {item_name}:")
    for position, record in enumerate(records, start=1):
        details = ", ".join(f"{key}: {value}" for key, value in record.items())
        print(f"{position}. {details}")

    while True:
        try:
            selection = int(input("Número: ").strip())
        except ValueError:
            print("Introduce un número válido.")
            continue

        if 1 <= selection <= len(records):
            return selection - 1
        print(f"Selecciona un número entre 1 y {len(records)}.")


def display_records(records: Sequence[Mapping[str, object]], title: str) -> None:
    print(f"\n=== {title} ===")
    if not records:
        print("No hay datos en memoria.")
        return

    for position, record in enumerate(records, start=1):
        details = ", ".join(f"{key}: {value}" for key, value in record.items())
        print(f"{position}. {details}")