-- ============================================================
-- CSDL quản lý đồ án tốt nghiệp (MySQL 8.0+)
-- Tạo mới database: demo_quan_ly_do_an
-- Chạy lại file này sẽ xóa database hiện tại và toàn bộ dữ liệu bên trong.
-- Chỉ dùng khi muốn tạo mới hoàn toàn.
-- ============================================================

DROP DATABASE IF EXISTS demo_quan_ly_do_an;

CREATE DATABASE IF NOT EXISTS demo_quan_ly_do_an
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE demo_quan_ly_do_an;

CREATE TABLE IF NOT EXISTS SINHVIEN (
    ma_sinh_vien VARCHAR(20) NOT NULL,
    ho_ten       VARCHAR(100) NOT NULL,
    email        VARCHAR(255) NULL,
    lop          VARCHAR(50) NULL,
    nganh        VARCHAR(100) NULL,
    so_dien_thoai VARCHAR(20) NULL,
    PRIMARY KEY (ma_sinh_vien),
    UNIQUE KEY uq_sinhvien_email (email)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS DETAI (
    ma_de_tai       VARCHAR(20) NOT NULL,
    ten_de_tai      VARCHAR(200) NOT NULL,
    mo_ta           TEXT NULL,
    giang_vien_huong_dan VARCHAR(100) NULL,
    so_luong_toi_da INT UNSIGNED NOT NULL DEFAULT 1,
    trang_thai      ENUM('MO_DANG_KY', 'DA_DONG') NOT NULL DEFAULT 'MO_DANG_KY',
    PRIMARY KEY (ma_de_tai),
    CONSTRAINT chk_detai_so_luong CHECK (so_luong_toi_da > 0)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS DANGKY (
    ma_dang_ky    BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ma_sinh_vien  VARCHAR(20) NOT NULL,
    ma_de_tai     VARCHAR(20) NOT NULL,
    ngay_dang_ky  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    trang_thai    ENUM('DA_DANG_KY', 'DA_HUY') NOT NULL DEFAULT 'DA_DANG_KY',
    ma_sinh_vien_dang_ky VARCHAR(20) GENERATED ALWAYS AS (
        CASE WHEN trang_thai = 'DA_DANG_KY' THEN ma_sinh_vien ELSE NULL END
    ) STORED,
    PRIMARY KEY (ma_dang_ky),
    -- Một sinh viên không thể đăng ký cùng một đề tài hai lần.
    UNIQUE KEY uq_dangky_sinhvien_detai (ma_sinh_vien, ma_de_tai),
    -- Chỉ một đăng ký còn hiệu lực cho mỗi sinh viên; DA_HUY tạo giá trị NULL.
    UNIQUE KEY uq_dangky_sinhvien_dang_ky (ma_sinh_vien_dang_ky),
    KEY idx_dangky_detai (ma_de_tai),
    CONSTRAINT fk_dangky_sinhvien
        FOREIGN KEY (ma_sinh_vien) REFERENCES SINHVIEN (ma_sinh_vien)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_dangky_detai
        FOREIGN KEY (ma_de_tai) REFERENCES DETAI (ma_de_tai)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Dữ liệu mẫu (có thể chạy lại mà không tạo bản ghi trùng).
INSERT INTO SINHVIEN (ma_sinh_vien, ho_ten, email, lop, nganh, so_dien_thoai)
VALUES
    ('SV001', 'Nguyen Van An', 'an.sv001@example.com', 'CNTT-K20', 'Cong nghe thong tin', '0900000001'),
    ('SV002', 'Tran Thi Binh', 'binh.sv002@example.com', 'CNTT-K20', 'Cong nghe thong tin', '0900000002')
ON DUPLICATE KEY UPDATE
    ho_ten = VALUES(ho_ten), email = VALUES(email), lop = VALUES(lop),
    nganh = VALUES(nganh), so_dien_thoai = VALUES(so_dien_thoai);

INSERT INTO DETAI (ma_de_tai, ten_de_tai, mo_ta, giang_vien_huong_dan, so_luong_toi_da, trang_thai)
VALUES
    ('DT001', 'Xay dung website quan ly thu vien', 'Ung dung web quan ly sach va muon tra.', 'ThS. Nguyen Van Huong', 1, 'MO_DANG_KY'),
    ('DT002', 'Ung dung theo doi tien do do an', 'Ung dung ho tro theo doi tien do thuc hien do an.', 'ThS. Tran Thi Mai', 2, 'MO_DANG_KY')
ON DUPLICATE KEY UPDATE
    ten_de_tai = VALUES(ten_de_tai), mo_ta = VALUES(mo_ta),
    giang_vien_huong_dan = VALUES(giang_vien_huong_dan),
    so_luong_toi_da = VALUES(so_luong_toi_da), trang_thai = VALUES(trang_thai);

-- Bỏ comment nếu muốn có sẵn một đăng ký mẫu:
-- INSERT INTO DANGKY (ma_sinh_vien, ma_de_tai)
-- VALUES ('SV001', 'DT001');
