#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    record = json.loads(line)
    record["ai_response"] = "TEST_OK"
    print(json.dumps(record))
