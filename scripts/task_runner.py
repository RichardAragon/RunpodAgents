import argparse
import os
from src.client import call_generate
from src.utils import ensure_dir, write_json
from src.config import settings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task", help="Instruction/prompt for the agent")
    ap.add_argument("--out", default="", help="Write JSON response to file (optional)")
    ap.add_argument("--max_tokens", type=int, default=settings.default_max_tokens)
    ap.add_argument("--temperature", type=float, default=settings.default_temperature)
    ap.add_argument("--api_url", default=os.getenv("LOCAL_LLM_URL", "http://localhost:8000/generate"))
    ap.add_argument("--timeout_s", type=int, default=settings.request_timeout_s)
    args = ap.parse_args()

    resp = call_generate(
        prompt=args.task,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        api_url=args.api_url,
        timeout_s=args.timeout_s,
    )

    if args.out:
        ensure_dir(os.path.dirname(args.out) or ".")
        write_json(args.out, resp)
        print(f"Wrote: {args.out}")
    else:
        print(resp.get("text") if isinstance(resp, dict) else resp)

if __name__ == "__main__":
    main()
