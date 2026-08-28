from pathlib import Path
import uuid

SCRIPTS_DIR = Path("/scripts")
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


def save_script(file_name: str, content: bytes) -> dict:
    execution_id = str(uuid.uuid4())[:8]

    execution_path = SCRIPTS_DIR / execution_id
    execution_path.mkdir(parents=True, exist_ok=True)

    script_path = execution_path / file_name
    script_path.write_bytes(content)

    return {
        "execution_id": execution_id,
        "script_path": str(script_path)
    }