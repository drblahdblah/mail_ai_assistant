"""
# Script to parse and index all emails
"""

import os
import json
import mailbox
from pathlib import Path
from email import policy
from email.parser import BytesParser
from tqdm import tqdm

# Customize to your Mail version
MAIL_BASE_DIR = os.path.expanduser('/Users/davidjones/Library/Mail/V10')  # V10 or V9 depending on macOS
OUTPUT_DIR = Path('data/raw_emails')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def parse_emlx_file(file_path):
    with open(file_path, 'rb') as f:
        try:
            # Read the first line to get the byte count
            first_line = f.readline()
            byte_count = int(first_line.strip())
            
            # Read the actual email content (next byte_count bytes)
            email_content = f.read(byte_count)
            
            # Parse the email content
            msg = BytesParser(policy=policy.default).parsebytes(email_content)
            
            # Extract body content
            body = ""
            if msg.is_multipart():
                body_part = msg.get_body(preferencelist=('plain', 'html'))
                if body_part:
                    body = body_part.get_content()
            else:
                body = msg.get_payload(decode=True)
                if isinstance(body, bytes):
                    body = body.decode('utf-8', errors='ignore')
            
            return {
                'subject': msg.get('subject'),
                'from': msg.get('from'),
                'to': msg.get('to'),
                'date': msg.get('date'),
                'body': body,
                'raw': email_content.decode('utf-8', errors='ignore')
            }
        except Exception as e:
            print(f'Error parsing {file_path}: {e}')
            return None

def find_emlx_files(base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.emlx'):
                yield os.path.join(root, file)

def main():
    files = list(find_emlx_files(MAIL_BASE_DIR))
    print(f'Found {len(files)} emails to process.')

    for path in tqdm(files, desc='Parsing emails'):
        parsed = parse_emlx_file(path)
        if parsed:
            file_name = os.path.basename(path).replace('.emlx', '') + '.json'
            out_path = OUTPUT_DIR / file_name
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(parsed, f, indent=2)

if __name__ == '__main__':
    main()
