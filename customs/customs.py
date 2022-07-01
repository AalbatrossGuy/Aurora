import subprocess, datetime

uptime: datetime.datetime


def version_info():
    version = 'No Data'
    date = 'No Data'
    git_log = subprocess.check_output(
        ['git', 'log', '-n', '1', '--date=format:"%d-%m-%Y %H:%M:%S"']).decode()
    for line in git_log.split('\n'):
        if line.startswith('commit'):
            version = line.split(' ')[1]
        elif line.startswith('Date'):
            date = line[5:].strip().replace('"', '')
        else:
            pass
    return version, date


def get_uptime():
    return uptime


def set_uptime(time: datetime.datetime):
    global uptime
    uptime = time


if __name__ == '__main__':
    print("Run as import.")
