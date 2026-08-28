from pathlib import Path
import uuid
import json

SCRIPTS_DIR = Path("/scripts")
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


def save_script(file_name: str, content: bytes):
    execution_id = str(uuid.uuid4())[:8]

    execution_path = SCRIPTS_DIR / execution_id
    execution_path.mkdir(parents=True, exist_ok=True)

    report_path = execution_path / "report"
    report_path.mkdir(exist_ok=True)

    script_path = execution_path / file_name

    script_path.write_bytes(content)

    metadata = {
        "execution_id": execution_id,
        "script_name": file_name,
    }

    (execution_path / "metadata.json").write_text(
        json.dumps(metadata, indent=2)
    )

    return {
        "execution_id": execution_id,
        "script_name": file_name,
        "script_path": str(script_path),
    }