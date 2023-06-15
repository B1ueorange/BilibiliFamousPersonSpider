import subprocess
import time


def main():

    flfl = 0
    cnt = 0
    while (flfl == 0):
        pl = subprocess.Popen("python Download.py")
        time.sleep(3600)
        cnt += 1
        pl.kill()


if __name__ == '__main__':
    main()