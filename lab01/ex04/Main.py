from QuanLySinhVien import QuanLySinhVien

qlsv = QuanLySinhVien()

while True:
    print("CHƯƠNG TRÌNH QUẢN LÝ SINH VIÊN")
    print("============== MENU ==============")
    print("1. Nhap sinh vien")
    print("2. Cap nhat sinh vien")
    print("3. Xoa sinh vien theo mssv")
    print("4. Tim kiem theo ten")
    print("5. Sap xep theo diem trung binh")
    print("6. Sap xep theo ten")
    print("7. Hien thi danh sach sinh vien")
    print("0. Thoat")
    print("===================================")
    choice = int(input("Nhap lua chon: "))
    
    if choice == 1:
        qlsv.nhapSinhVien()
    elif choice == 2:
        mssv = int(input("Nhap mssv: "))
        qlsv.updateSinhVien(mssv)
    elif choice == 3:
        mssv = int(input("Nhap mssv: "))
        if qlsv.deleteByID(mssv):
            print(f"Sinh vien co mssv {mssv} da bi xoa.")
        else:
            print(f"Sinh vien co mssv {mssv} khong ton tai.")
    elif choice == 4:
        ho_ten = input("Nhap ho ten: ")
        svs = qlsv.findByHoTen(ho_ten)
        qlsv.showAll(svs)
    elif choice == 5:
        qlsv.sortByDiemTB()
        print("Danh sach da duoc sap xep theo diem trung binh.")
    elif choice == 6:
        qlsv.sortByName()
        print("Danh sach da duoc sap xep theo ten.")
    elif choice == 7:
        qlsv.showAll(qlsv.getSinhVien())
    elif choice == 0:
        break
    else:
        print("Lua chon khong hop le, vui long thu lai!")
