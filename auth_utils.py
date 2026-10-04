import json
from pathlib import Path
from typing import Dict, Optional, Tuple


def get_users_file(path: Optional[str | Path] = None) -> Path:
    if path is None:
        base_dir = Path(__file__).resolve().parent
        return base_dir / "data" / "users.json"
    return Path(path)


def load_users(users_file: Optional[str | Path] = None) -> Dict[str, Dict[str, str]]:
    file_path = get_users_file(users_file)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        return {}
    with file_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_users(users: Dict[str, Dict[str, str]], users_file: Optional[str | Path] = None) -> None:
    file_path = get_users_file(users_file)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as handle:
        json.dump(users, handle, indent=2)


def register_user(username: str, password: str, full_name: str, users_file: Optional[str | Path] = None) -> Tuple[bool, str]:
    if not username or not password:
        return False, "Username and password are required."

    users = load_users(users_file)
    if username in users:
        return False, "This username already exists."

    users[username] = {"username": username, "password": password, "full_name": full_name or username}
    save_users(users, users_file)
    return True, f"User '{username}' registered successfully."


def authenticate_user(username: str, password: str, users_file: Optional[str | Path] = None) -> Optional[Dict[str, str]]:
    users = load_users(users_file)
    user = users.get(username)
    if user and user.get("password") == password:
        return user
    return None
