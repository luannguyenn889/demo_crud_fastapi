-- Chạy một lần trên database hiện có sau khi xử lý mọi sinh viên đang có
-- nhiều hơn một bản ghi DANGKY ở trạng thái DA_DANG_KY.
USE demo_quan_ly_do_an;

ALTER TABLE DANGKY
    ADD COLUMN ma_sinh_vien_dang_ky VARCHAR(20)
        GENERATED ALWAYS AS (
            CASE WHEN trang_thai = 'DA_DANG_KY' THEN ma_sinh_vien ELSE NULL END
        ) STORED,
    ADD UNIQUE KEY uq_dangky_sinhvien_dang_ky (ma_sinh_vien_dang_ky);
