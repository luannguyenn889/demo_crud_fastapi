export type Page = 'overview' | 'students' | 'topics' | 'registrations';

export type Student = {
  ma_sinh_vien: string;
  ho_ten: string;
  email: string | null;
  lop: string | null;
  nganh: string | null;
  so_dien_thoai: string | null;
};

export type Topic = {
  ma_de_tai: string;
  ten_de_tai: string;
  mo_ta: string | null;
  giang_vien_huong_dan: string | null;
  so_luong_toi_da: number;
  trang_thai: 'MO_DANG_KY' | 'DA_DONG';
};

export type Registration = {
  ma_dang_ky: number;
  ma_sinh_vien: string;
  ma_de_tai: string;
  ngay_dang_ky: string;
  trang_thai: 'DA_DANG_KY' | 'DA_HUY';
};
