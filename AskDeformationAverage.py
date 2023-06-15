
import os

class frm:
    def __init__(self, pos, h1, l1, h2, l2):
        self.pos = pos
        self.h1 = h1
        self.l1 = l1
        self.h2 = h2
        self.l2 = l2

def main():
    frame_dir = './frame'
    frame_list = os.listdir(frame_dir)
    cnt = 0
    sum = 0.0
    l = ''
    frame_change_list = []
    for i in frame_list:
        point_name = frame_dir + '/' + i + '/point.txt'
        if not os.path.exists(point_name):
            continue
        ter = []
        with open(point_name, 'rt', encoding='utf-8') as f:
            for line in f:
                tmp1 = line.split( )
                tmp2 = frm(int(tmp1[0]), int(tmp1[1]), int(tmp1[2]), int(tmp1[3]), int(tmp1[4]))
                ter.append(tmp2)
        le = len(ter)
        ll = ''
        for j in range(1, le):
            if(ter[j].pos != ter[j - 1].pos + 1):
                continue
            cnt += 1
            s0 = abs(ter[j - 1].h2 - ter[j - 1].h1) * abs(ter[j - 1].l2 - ter[j - 1].l1)
            s1 = abs(ter[j].h2 - ter[j].h1) * abs(ter[j].l2 - ter[j].l1)
            bili = s1 / s0
            l += i + ' ' + str(ter[j].pos) + ' ' + str(bili) + '\n'
            ll += i + ' ' + str(ter[j].pos) + ' ' + str(bili) + '\n'
            frame_change_list.append(bili)
            sum += abs(1 - bili)
        with open(frame_dir + '/' + i + '/deformation.txt', 'w', encoding='utf-8') as f:
            f.writelines(ll)
    frame_change_list.sort()
    with open('./Average.txt', 'w', encoding='utf-8') as f:
        f.write(str(sum) + ' ' + str(cnt) + ' ' + str(sum / cnt))
    # le = len(frame_change_list)
    # for i in range(0, le):
    #     l += str(frame_change_list[i]) + '\n'
    with open('./face_deformation.txt', 'w', encoding='utf-8') as f:
        f.writelines(l)

if __name__ == '__main__':
    main()