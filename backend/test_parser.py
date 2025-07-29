#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

from scripts.ingest_emails import parse_emlx_file
import json

# Test our parsing function
result = parse_emlx_file('test_sample.emlx')
if result:
    print("Parsing successful!")
    print("Subject:", result['subject'])
    print("From:", result['from'])
    print("To:", result['to'])
    print("Date:", result['date'])
    print("Body:", result['body'])
    print("\nFull JSON:")
    print(json.dumps(result, indent=2))
else:
    print("Parsing failed!")
