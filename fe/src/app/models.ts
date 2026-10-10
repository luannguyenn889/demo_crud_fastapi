// Các trang chính trong ứng dụng Frontend
export type Page = 'overview' | 'students' | 'topics' | 'registrations';

// Kiểu dữ liệu Sinh viên (Student)
export type Student = {
  ma_sinh_vien: string;       // Mã số sinh viên (khóa chính)
  ho_ten: string;             // Họ và tên sinh viên
  email: string | null;       // Email liên hệ
  lop: string | null;         // Lớp sinh hoạt
  nganh: string | null;       // Chuyên ngành học
  so_dien_thoai: string | null; // Số điện thoại liên hệ
};

// Kiểu dữ liệu Đề tài tốt nghiệp (Topic)
export type Topic = {
  ma_de_tai: string;          // Mã đề tài (khóa chính)
  ten_de_tai: string;         // Tên đề tài
  mo_ta: string | null;       // Nội dung mô tả đề tài
  giang_vien_huong_dan: string | null; // Tên giảng viên hướng dẫn
  so_luong_toi_da: number;    // Số lượng sinh viên tối đa được nhận
  trang_thai: 'MO_DANG_KY' | 'DA_DONG'; // Trạng thái mở hoặc đóng đăng ký
};

// Kiểu dữ liệu Đăng ký đề tài (Registration)
export type Registration = {
  ma_dang_ky: number;         // Mã số đăng ký tự tăng (ID)
  ma_sinh_vien: string;       // Mã sinh viên thực hiện đăng ký
  ma_de_tai: string;          // Mã đề tài được đăng ký
  ngay_dang_ky: string;       // Thời gian đăng ký (định dạng ISO string)
  trang_thai: 'DA_DANG_KY' | 'DA_HUY'; // Trạng thái: đang hiệu lực hoặc đã hủy
};

