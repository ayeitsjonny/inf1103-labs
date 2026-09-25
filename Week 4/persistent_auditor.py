def load_inventory(filename):
    """Reads previously saved inventory state.
    Returns (total, history) as (int, list).
    If the file doesn't exist, starts empty instead of crashing.
    """
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return 0, []
 
    total = 0
    history = []
 
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("TOTAL,"):
            total = int(line.split(",", 1)[1])
        else:
            history.append(int(line))
 
    return total, history