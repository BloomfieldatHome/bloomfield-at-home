#!/usr/bin/env python3
"""Generate images with the Gemini API for requests in tools/ai-images/requests.json.
Runs in GitHub Actions; the key comes from the GEMINI_API_KEY secret and is never printed."""
import base64, json, os, sys, urllib.request, urllib.error
from pathlib import Path

KEY = os.environ.get("GEMINI_API_KEY", "")
BASE = "https://generativelanguage.googleapis.com/v1beta"
HERE = Path(__file__).parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
LOG = HERE / "last_run.txt"

def call(url, data=None):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None,
                                 headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())

def pick_model():
    models = call(f"{BASE}/models?pageSize=200").get("models", [])
    names = [m["name"] for m in models if "generateContent" in m.get("supportedGenerationMethods", [])
             and "image" in m["name"] and "flash" in m["name"]]
    names.sort(key=lambda n: ("preview" in n, "lite" in n, n), reverse=False)
    # prefer the newest non-preview flash image model
    names.sort(key=lambda n: [int(x) if x.isdigit() else 0 for x in n.replace("-", ".").split(".")], reverse=True)
    names.sort(key=lambda n: ("lite" in n, "preview" in n))  # full flash model first, lite as fallback
    return names

def main():
    log = []
    if not KEY:
        LOG.write_text("No GEMINI_API_KEY secret available.\n"); return
    reqs = json.loads((HERE / "requests.json").read_text())
    try:
        candidates = pick_model()
    except urllib.error.HTTPError as e:
        LOG.write_text(f"Model list failed: HTTP {e.code} {e.read()[:300]!r}\n"); return
    log.append("Image models available: " + ", ".join(candidates))
    for r in reqs:
        target = OUT / f"{r['id']}.png"
        if target.exists():
            continue
        done = False
        for model in candidates:
            body = {"contents": [{"parts": [{"text": r["prompt"]}]}],
                    "generationConfig": {"responseModalities": ["IMAGE"],
                                         "imageConfig": {"aspectRatio": r.get("aspect", "2:3")}}}
            try:
                res = call(f"{BASE}/{model}:generateContent", body)
            except urllib.error.HTTPError as e:
                log.append(f"{r['id']}: {model} -> HTTP {e.code} {e.read()[:300]!r}")
                continue
            for part in res.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                if "inlineData" in part:
                    target.write_bytes(base64.b64decode(part["inlineData"]["data"]))
                    log.append(f"{r['id']}: OK with {model}"); done = True; break
            if done: break
            log.append(f"{r['id']}: {model} returned no image")
        if not done:
            log.append(f"{r['id']}: FAILED")
    LOG.write_text("\n".join(log) + "\n")

main()
