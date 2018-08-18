import re

filename_raw_list = 'filelist_diarios_raw.txt'
matcher = re.compile('^.*\d+\s(Diarios.*)$')
with open(filename_raw_list, 'r') as f:
    for line in f:
        result = matcher.match(line)
        if result:
            print(result.group(1))

