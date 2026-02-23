import os
import time
from pathlib import Path
from .config import settings
from .client import call_generate
from .utils import ensure_dir, now_iso, write_json

def run_forever(poll_s: float = 1.0) -> None:
    ensure_dir(settings.tasks_incoming)
    ensure_dir(settings.tasks_outgoing)
    ensure_dir(settings.artifacts_dir)

    seen = set()

    while True:
        for p in Path(settings.tasks_incoming).glob("*.txt"):
            if p.name in seen:
                continue

            task = p.read_text(encoding="utf-8").strip()
            if not task:
                seen.add(p.name)
                continue

            try:
                resp = call_generate(
                    prompt=task,
                    max_tokens=settings.default_max_tokens,
                    temperature=settings.default_temperature,
                    timeout_s=settings.request_timeout_s,
                )
                out = {
                    "task_file": p.name,
                    "task": task,
                    "result": resp,
                    "ts": now_iso(),
                }
                out_path = os.path.join(settings.tasks_outgoing, p.stem + ".json")
                write_json(out_path, out)
            except Exception as e:
                out = {"task_file": p.name, "task": task, "error": str(e), "ts": now_iso()}
                out_path = os.path.join(settings.tasks_outgoing, p.stem + ".error.json")
                write_json(out_path, out)

            seen.add(p.name)

        time.sleep(poll_s)
