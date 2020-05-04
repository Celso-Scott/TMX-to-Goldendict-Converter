#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
import re

# Run regex search and replacements versions 1 and 2
def replacements(tm):
    # Remove tags
    tm = re.sub(r'<tei:milestone xml:id="UT22084-\d+-\d+-\d+"/>', '', tm)
    tm = re.sub(r'<tei:note xml:id="UT22084-\d+-\d+-\d+"/>', '', tm)
    tm = re.sub(r'<tei:ref folio="[Ff]\.\d+\.[ab]"/>', '', tm)
    # Normalize spaces and remove linebreaks
    tm = re.sub(r'\s+', ' ', tm)
    # Format lines and reinsert linebreaks
    tm = re.sub(r'<tu[>\s][^་]+?"folio">[Ff](\.\d+\.[ab])[^་]+?<seg>([^<]+)</seg>[^་]+?<seg>([^<]+)</seg>[^་]+?</tu>\s+', r'\2\t\3 (F\1)\n', tm)
    # Remove front and end matter
    tm = re.sub(r'<tmx[^་]+?(<body>)\s*', '', tm)
    tm = re.sub(r'</body>\s*</tmx>\s*', '', tm)
    # Add Toh and info
    tm = re.sub(r'\((F\.\d+\.[ab])\)', r'(Toh - \1)', tm)
    return tm

# Add the toh number to the end of each entry
def add_toh(tm, toh_to_add):
    lines = tm.split('\n')
    for num, s in enumerate(lines):
        if '(Toh ' in s:
            new = ''
            for chunk in re.split(r'(\(Toh )', lines[num]):
                if '(Toh ' in chunk:
                    new += '(Toh '
                    new += toh_to_add
                    new += ' '
                else:
                    new += chunk
            lines[num] = new
    lines = '\n'.join(lines)
    return lines

# This is the primary function in the script to process all TMX files 
# in directory "input_84000_tms" and write to "ready_to_merge_84000"
def preprocess(in_dir, out_dir):
    # get path for TMX in input_84000_tms
    for file in in_dir.glob('*.tmx'):
        if not file.is_file():
            exit(f'{file} is missing.\nExiting')

        # access toh number from file
        get_fname = file.name
        toh_to_add = re.sub(r'Toh_(\d+).+', r'\1', get_fname)
        
        # process TMX v1 and 2
        tm = file.read_text(encoding='utf-8-sig')
        tm = replacements(tm)
        tm = add_toh(tm, toh_to_add)
        to_file = out_dir / file.name
        to_file.write_text(tm, encoding='utf-8-sig')


if __name__ == '__main__':
    in_dir = Path('input_84000_tms')
    in_dir.mkdir(exist_ok=True)

    out_dir = Path('ready_to_merge_84000')
    out_dir.mkdir(exist_ok=True, parents=True)
    # empty output folder at each run
    for o in out_dir.parent.glob('*.tmx'):
        o.unlink()
    for o in out_dir.glob('*.tmx'):
        o.unlink()

    preprocess(in_dir, out_dir)
