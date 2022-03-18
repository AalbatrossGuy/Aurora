# Start_info.py
import subprocess
from datetime import datetime

def version_info():
    version = 'No Data'
    date = 'No Data'
    gitlog = subprocess.check_output(
        ['git', 'log', '-n', '1', '--date=iso']).decode()
    for line in gitlog.split('\n'):
        if line.startswith('commit'):
            version = line.split(' ')[1]
        elif line.startswith('Date'):
            date = line[5:].strip()
            date = date.replace(' +', '+').replace(' ', 'T')
        else:
            pass
    return version, date


if __name__ == '__main__':
    print("Run as import.")
