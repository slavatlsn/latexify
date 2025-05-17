from pos_detect import data
from sym_detect import symbol

yolo_label_map = {
    0: "(", 1: ")", 2: "a", 3: "+", 4: "b", 5: "c", 6: "d", 7: "/", 8: "e", 9: "8",
    10: "=", 11: "f", 12: "5", 13: "4", 14: "g", 15: "h", 16: "i", 17: "j", 18: "k",
    19: "l", 20: "m", 21: "n", 22: "9", 23: "o", 24: "1", 25: "p", 26: "q", 27: "r",
    28: "s", 29: "7", 30: "6", 31: "-", 32: "t", 33: "3", 34: "2", 35: "u", 36: "v",
    37: "w", 38: "x", 39: "y", 40: "z", 41: "0", 42: "*", 43: "A", 44: "B", 45: "C",
    46: "D", 47: "E", 48: "F", 49: "G", 50: "H", 51: "I", 52: "J", 53: "K", 54: "L",
    55: "M", 56: "N", 57: "O", 58: "P", 59: "Q", 60: "R", 61: "S", 62: "T", 63: "U",
    64: "V", 65: "W", 66: "X", 67: "Y", 68: "Z", 69: "x", 70: "/"
}

res = {
    ('o', '0'): '0',
    ('z', '2'): '2',
    ('z', '3'): '2',
    ('+', '4'): '+',
    ('-', '4'): '+',
    ('-', '2'): 'L'
}

keys = set(res.keys())


def process(arg):
    inp = (arg[1], arg[2])
    if arg[1] == arg[2]:
        r = arg[1]
    elif inp in keys:
        r = res[inp]
    else:
        if arg[2].isdigit() or arg[1] in '-()*/+':
            if arg[3] < 0.2:
                r = arg[1]
            else:
                r = arg[2]
        else:
            if arg[3] < 0.62:
                r = arg[1]
            else:
                r = arg[2]
    return arg[0], r, arg[3]


def get_latex(path):
    img_data = data(path)
    if not img_data[0]:
        return ['']
    new_data = []
    imgh = 0
    imgl = 0
    i = 0
    for img, cls in zip(img_data[0], img_data[1]):
        if img is not None:
            symdata = img[1], symbol(img[0])[0], yolo_label_map[int(cls[0])], round(cls[1].item(), 2)
            imgh += abs(img[1][3] - img[1][1])
            imgl += abs(img[1][2] - img[1][0])
            new_data.append(process(symdata))
            i += 1

    def getpos(obj):
        return (i * (obj[0][1] + obj[0][3]) // (7 * imgh // 3), 9 * i * (obj[0][0] + obj[0][2]) // (imgl * 10)), obj[1], obj[2]

    def form(obj):
        return obj[0][1], (obj[1], obj[2])

    new_data = list(map(getpos, new_data))
    strings = []
    final = []
    new_data.sort(key=lambda x: (x[0], x[2]))
    prev = new_data[0][0][0]
    now = [form(new_data[0])]
    for el in new_data[1:]:
        if el[0][0] == prev:
            now.append(form(el))
        else:
            strings.append(now)
            now = [form(el)]
        prev = el[0][0]
    strings.append(now)
    for s in strings:
        d = dict(s)
        buf = ''
        for e in d.keys():
            buf += d[e][0]
        final.append(buf)
    return final
