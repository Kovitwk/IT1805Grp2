lines = []
text = {}
k = 1
bmi = 17

if bmi < 18:
    file = open('under.txt', 'r')
    content = file.readline()
    while content != "":
        content = file.readline()
        lines.append(content)
        print(content)
    file.close()
    for i in range(len(lines)):
        text[k] = lines[i]
        i += 2
        k += 1
    print(text)

if 18 <= bmi <= 25:
    file = open('normal.txt', 'r')
    content = file.readline()
    while content != "":
        content = file.readline()
        lines.append(content)
        print(content)
    file.close()
    for i in range(len(lines)):
        text[k] = lines[i]
        i += 2
        k += 1
    print(text)

if bmi > 25:
    file = open('over.txt', 'r')
    content = file.readline()
    while content != "":
        content = file.readline()
        lines.append(content)
        print(content)
    file.close()
    for i in range(len(lines)):
        text[k] = lines[i]
        i += 2
        k += 1
    print(text)
