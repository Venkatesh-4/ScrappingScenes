def clean_value(value, dtype=str):
    """Convert '-' to None and cast to the specified dtype if possible."""
    if value == "-":
        return None
    try:
        return dtype(value.strip())
    except (ValueError, TypeError):
        return None
    
if __name__ == "__main__":
    clean_value