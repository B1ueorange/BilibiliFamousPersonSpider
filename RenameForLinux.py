import os.path


def change(pos):
    new_name = pos.encode('gbk', errors='surrogateescape')
    new_name = new_name.decode('utf-8', errors='surrogateescape')
    # print(new_name)
    if(os.path.isfile(pos)):
        os.rename(pos, new_name)
        return
    file_list = os.listdir(pos)
    for i in file_list:
        change(pos + '/' + i)
    os.rename(pos, new_name)

def main():
    change('./face')

if __name__ == '__main__':
    main()