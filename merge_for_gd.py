import glob

read_files = glob.glob("ready_to_merge_84000\*.tmx")
read_files += glob.glob("ready_to_merge_other\*.tmx")

with open("merged.txt", "w", encoding='utf-8-sig') as outfile:
    for f in read_files:
        with open(f, "r", encoding='utf-8-sig') as infile:
            outfile.write(infile.read())
            
