print("Nhập dòng văn bản (nhập 'done' để kết thúc):")
lines = []
while True:
    line = input()
    if line.lower() == 'done':
        break
    lines.append(line)
print("Dòng văn bản đã nhập:")
for line in lines:
    print(line.upper())