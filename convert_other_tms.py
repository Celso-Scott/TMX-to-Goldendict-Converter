#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
import re

# Run regex search and replacements
def replacements(tm):
    # Remove front and end matter
    tm = re.sub(r'<\?xml.+', '', tm)
    tm = re.sub(r'<tmx[^་]+?(<body>)\s*', '', tm)
    tm = re.sub(r'</body>\s*</tmx>\s*', '', tm)
    # Normalize spaces and remove linebreaks
    tm = re.sub(r'\s+', ' ', tm)
    # Format lines and reinsert linebreaks
    tm = re.sub(r'<tu[>\s][\s\S]+?<seg>([\s\S]+?)</seg>[\s\S]+?<seg>([\s\S]+?)</seg>[\s\S]+?</tu>\s*', r'\1\t\2\n', tm)
    return tm


# This is the primary function in the script to process all TMX files 
# in directory "input_other_tms" and write to "ready_to_merge_other"
def preprocess(in_dir, out_dir):
    # get path for TMX in input_other_tms
    for file in in_dir.glob('*.tmx'):
        if not file.is_file():
            exit(f'{file} is missing.\nExiting')

        # process TMX v1 and 2
        tm = file.read_text(encoding='utf-8-sig')
        tm = replacements(tm)
        to_file = out_dir / file.name
        to_file.write_text(tm, encoding='utf-8-sig')


if __name__ == '__main__':
    in_dir = Path('input_other_tms')
    in_dir.mkdir(exist_ok=True)

    out_dir = Path('ready_to_merge_other')
    out_dir.mkdir(exist_ok=True, parents=True)
    # empty output folder at each run
    for o in out_dir.parent.glob('*.tmx'):
        o.unlink()
    for o in out_dir.glob('*.tmx'):
        o.unlink()

    preprocess(in_dir, out_dir)
