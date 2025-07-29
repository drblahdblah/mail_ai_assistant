#!/usr/bin/env python3

import os
import json
import glob
from pathlib import Path
from email import policy
from email.parser import BytesParser
from tqdm import tqdm

def reprocess_email_json(json_file_path):
    """Reprocess a single JSON file to extract proper email fields"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get the raw content
        raw_content = data.get('raw', '')
        if not raw_content:
            print(f"No raw content in {json_file_path}")
            return None
        
        # The raw content starts with byte count, we need to extract the actual email
        lines = raw_content.split('\n')
        if not lines:
            return None
            
        # First line should be the byte count
        try:
            byte_count = int(lines[0].strip())
        except (ValueError, IndexError):
            print(f"Invalid byte count in {json_file_path}")
            return None
        
        # Join the rest and take only the specified number of bytes
        email_content = '\n'.join(lines[1:])
        email_bytes = email_content.encode('utf-8')[:byte_count]
        
        # Parse the email content
        msg = BytesParser(policy=policy.default).parsebytes(email_bytes)
        
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
        
        # Create updated data
        updated_data = {
            'subject': msg.get('subject'),
            'from': msg.get('from'),
            'to': msg.get('to'),
            'date': msg.get('date'),
            'body': body,
            'raw': email_bytes.decode('utf-8', errors='ignore')
        }
        
        return updated_data
        
    except Exception as e:
        print(f'Error reprocessing {json_file_path}: {e}')
        return None

def main():
    # Process all JSON files in the raw_emails directory
    json_files = glob.glob('data/raw_emails/*.json')
    print(f'Found {len(json_files)} JSON files to reprocess.')
    
    success_count = 0
    error_count = 0
    
    for json_file in tqdm(json_files, desc='Reprocessing emails'):
        updated_data = reprocess_email_json(json_file)
        if updated_data:
            # Check if we actually extracted the fields
            if updated_data['subject'] or updated_data['from'] or updated_data['to']:
                # Write back the updated data
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(updated_data, f, indent=2)
                success_count += 1
            else:
                print(f"No email fields extracted from {json_file}")
                error_count += 1
        else:
            error_count += 1
    
    print(f"\nReprocessing complete!")
    print(f"Successfully updated: {success_count} files")
    print(f"Errors: {error_count} files")

if __name__ == '__main__':
    main()
