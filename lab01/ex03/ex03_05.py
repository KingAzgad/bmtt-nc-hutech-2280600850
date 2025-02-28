def dem_so_lan_xuat_hien(lst):
    cuont_dict = {}
    for item in lst:
        if item in cuont_dict:
            cuont_dict[item] += 1
        else:
            cuont_dict[item] = 1
    return cuont_dict
input_string = input("Nhập danh sách các từ, cách nhau bởi dấu cách: ")
words_list = input_string.split()

so_lan_xuat_hien = dem_so_lan_xuat_hien(words_list)
print("Số lần xuất hiện của mỗi từ trong danh sách là:", so_lan_xuat_hien)