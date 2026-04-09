#!/usr/bin/env python3

import sys
import csv
import requests

# ===== CONFIG =====
OLLAMA_URL = "http://192.168.1.37:11434/api/generate"
MODEL = "phi3"

# ===== READ INPUT =====
reader = csv.DictReader(sys.stdin)

if not reader.fieldnames:
    sys.exit(0)

fieldnames = reader.fieldnames + ["ai_response"]

writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

# ===== PROCESS ROWS =====
for row in reader:
    prompt = row.get("prompt", "")

    # Default response in case everything fails
    response = "ERROR: no response"

    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 80,     # limit response size (faster)
                    "temperature": 0.2     # stable SOC output
                }
            },
            timeout=120   # increase timeout (important)
        )

        # If HTTP failed
        if r.status_code != 200:
            response = f"ERROR: HTTP {r.status_code} - {r.text}"

        else:
            try:
                data = r.json()
                response = data.get("response")

                # Fallback if JSON structure weird
                if not response:
                    response = str(data)

            except Exception:
                # If JSON fails, use raw text
                response = r.text

    except requests.exceptions.Timeout:
        response = "ERROR: Ollama timeout"

    except requests.exceptions.ConnectionError:
        response = "ERROR: Cannot connect to Ollama"

    except Exception as e:
        response = f"ERROR: {str(e)}"

    # Always return something (prevents Splunk crash)
    row["ai_response"] = response
    writer.writerow(row)
