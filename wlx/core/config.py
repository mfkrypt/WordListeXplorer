from pathlib import Path
import json

CONFIG_DIR = Path.home() / ".wlx"
CONFIG_PATH = CONFIG_DIR / "config.json"

def init_config():
    CONFIG_DIR.mkdir(exist_ok=True)

    if not CONFIG_PATH.exists():
        default_config = {
            "wordlist_dirs": []
        }

        with open(CONFIG_PATH, "w") as f:
            json.dump(default_config, f, indent=4)


def load_config():
    init_config()

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
 
      
def add_directory(path: str):
    config = load_config()
    path = str(Path(path).resolve())

    if path not in config["wordlist_dirs"]:
        config["wordlist_dirs"].append(path)
        save_config(config)
        return True

    return False


def get_directories():
    config = load_config()
    return config.get("wordlist_dirs", [])


def remove_directory_by_index(index: int):
    config_data = load_config()
    dirs = config_data["wordlist_dirs"]

    if index < 1 or index > len(dirs):
        return None

    removed = dirs.pop(index - 1)
    save_config(config_data)

    return removed
