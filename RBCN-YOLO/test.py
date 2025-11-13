path = 'E:/PycharmProjects/pointnetplus/syau_single_maize/newdata/'
save = 'I:/newsjz/'
f = open("I:/sjzdata/list.txt", "r")
listlines = f.readlines()  # 读取全部内容
for listline in listlines:
    if listline[-1] == '\n':
        txtpath = listline[:-1] + '.txt'
    else:
        txtpath = listline + '.txt'
    txtfile = open(path + txtpath, "r")
    savefile = open(save + txtpath, mode='w')
    length = len(lines)
    i = 1
    for line in lines:
        if i == length:
            classes = line[-8:]
        else:
            classes = line[-9:-1]
        if classes != '0.000000':
            if i == length:
                newline = line[:-8] + '1.000000'
            else:
                newline = line[:-9] + '1.000000'
        else:
            if i == length:
                newline = line
            else:
                newline = line[:-1]
        savefile.write(newline + '\n')
        i = i + 1

    savefile.close()