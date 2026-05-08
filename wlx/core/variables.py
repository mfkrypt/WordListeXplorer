from pathlib import Path

WLX_DIR = Path.home() / ".wlx"
SESSION_FILE = WLX_DIR / "session.env"


def load_variables():
    """
    Load active WLX session variables.
    """

    if not SESSION_FILE.exists():
        return {}

    variables = {}

    with open(SESSION_FILE, "r") as f:

        for line in f:

            line = line.strip()

            if not line or "=" not in line:
                continue

            key, value = line.split("=", 1)

            variables[key] = value

    return variables