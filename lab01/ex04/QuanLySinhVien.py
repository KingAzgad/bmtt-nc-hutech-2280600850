from SinhVien import SinhVien

class QuanLySinhVien:
    listSinhVien = []
    
    def generateID(self):
        maxID = 1
        if self.soLuongSinhVien() > 0:
            maxID = self.listSinhVien[0].mssv
            for sv in self.listSinhVien:
                if sv.mssv > maxID:
                    maxID = sv.mssv
            maxID += 1
        return maxID
    
    def soLuongSinhVien(self):
        return len(self.listSinhVien)
    
    def nhapSinhVien(self):
        mssv = self.generateID()
        ho_ten = input("Nhap ho ten: ")
        sex = input("Nhap gioi tinh: ")
        major = input("Nhap nganh hoc: ")
        diemTB = float(input("Nhap diem trung binh: "))
        sv = SinhVien(mssv, ho_ten, sex, major, diemTB)
        self.xepLoaiHocLuc(sv)
        self.listSinhVien.append(sv)
        
    def updateSinhVien(self, mssv):
        sv = self.findByID(mssv)
        if sv is not None:
            ho_ten = input("Nhap ho ten: ")
            sex = input("Nhap gioi tinh: ")
            major = input("Nhap nganh hoc: ")
            diemTB = float(input("Nhap diem trung binh: "))
            sv.ho_ten = ho_ten
            sv.sex = sex
            sv.major = major
            sv.diemTB = diemTB
            self.xepLoaiHocLuc(sv)
        else:
            print(f"Sinh vien co mssv {mssv} khong ton tai")
            
    def sortById(self):
        self.listSinhVien.sort(key=lambda x: x.mssv)
        
    def sortByName(self):
        self.listSinhVien.sort(key=lambda x: x.ho_ten)
        
    def sortByDiemTB(self):
        self.listSinhVien.sort(key=lambda x: x.diemTB)
        
    def findByID(self, mssv):
        for sv in self.listSinhVien:
            if sv.mssv == mssv:
                return sv
        return None
    
    def findByHoTen(self, ho_ten):
        listSV = [sv for sv in self.listSinhVien if ho_ten.upper() in sv.ho_ten.upper()]
        return listSV
    
    def deleteByID(self, mssv):
        sv = self.findByID(mssv)
        if sv:
            self.listSinhVien.remove(sv)
            return True
        return False
            
    def xepLoaiHocLuc(self, sv):
        if sv.diemTB >= 8:
            sv.hocluc = "Gioi"
        elif sv.diemTB >= 6.5:
            sv.hocluc = "Kha"
        elif sv.diemTB >= 5:
            sv.hocluc = "Trung binh"
        else:
            sv.hocluc = "Yeu"
            
    def showAll(self, listSv):
        print("{:<8} {:<18} {:<8} {:<8} {:<8} {:<8}".format("MSSV", "Ho ten", "Gioi tinh", "Nganh hoc", "Diem TB", "Hoc luc"))
        if len(listSv) > 0:
            for sv in listSv:
                print("{:<8} {:<18} {:<8} {:<8} {:<8} {:<8}".format(sv.mssv, sv.ho_ten, sv.sex, sv.major, sv.diemTB, sv.hocluc))
        print("\n")
        
    def getSinhVien(self):
        return self.listSinhVien
