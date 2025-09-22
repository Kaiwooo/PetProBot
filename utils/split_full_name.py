def split_full_name(full_name: str):
    parts = full_name.strip().split()
    last_name = parts[0].capitalize() if len(parts) >= 1 else ""
    first_name = parts[1].capitalize() if len(parts) >= 2 else ""
    second_name = parts[2].capitalize() if len(parts) >= 3 else ""
    return last_name, first_name, second_name