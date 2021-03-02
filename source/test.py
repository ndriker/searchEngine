# ['calcul', 'paschk', 'fabian', 'bayer', 'christian', 'uwe', 'dick', 'olaf', 'lohweg', 'volker', 'sensorlos', 'zustandsã¼berwachung', 'synchronmotoren', 'bd', 'hoffmann', 'frank', 'hãœllermeier', 'eyk', 'hrsg', '23', 'karlsruh', 'kit', 'scientif', 'schriftenreih', 'des']
with open("inverted_index2.txt") as f:
    positions = [1474487]
    for i in positions:
        f.seek(i)
        print(f.readline().strip())
    # count = 0
    # for line in f:
    #     print(len(line))
    #     count += 1
    #     if count == 23:
    #         break

# list_words = []
# with open("inverted_index2.txt") as f:
#     for line in f:
#         if '$' not in line and ',' not in line:
#             list_words.append(line.strip())
#     # print(len(list_words))
#     list = list_words[0:91735]
#     temp_list = dict()
#     with open("index_of_index2.txt") as f2:
#         for line in f2:
#             token = line.split()[0]
#             temp_list[token] = line.split()[1]
#     readline_list = []
#     for key_word in list:
#         if key_word in temp_list:
#             f.seek(int(temp_list[key_word]))
#             readline_list.append((f.readline().strip()))
#     print(readline_list == list)
    # print("list is ", list)
