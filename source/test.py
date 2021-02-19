with open("inverted_index.txt") as f:
    positions = [0,201,278]
    for i in positions:
        f.seek(i)
        print(f.readline().strip())
    # count = 0
    # for line in f:
    #     print(len(line))
    #     count += 1
    #     if count == 23:
    #         break