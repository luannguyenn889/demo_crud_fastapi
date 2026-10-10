import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Registration } from '../models';

// Kiểu dữ liệu gửi lên khi đăng ký đề tài
export type RegistrationInput = {
  ma_sinh_vien: string; // Mã sinh viên
  ma_de_tai: string;    // Mã đề tài muốn đăng ký
};

@Injectable({
  providedIn: 'root',
})
export class RegistrationApi {
  private readonly http = inject(HttpClient);
  // Địa chỉ API của DangKy Service (chạy ở cổng 8003)
  private readonly endpoint = 'http://localhost:8003/api/v1/dang-ky';

  // Lấy danh sách toàn bộ các lượt đăng ký
  list(): Observable<Registration[]> {
    return this.http.get<Registration[]>(this.endpoint);
  }

  // Tạo mới một lượt đăng ký đề tài
  create(input: RegistrationInput): Observable<Registration> {
    return this.http.post<Registration>(this.endpoint, input);
  }

  // Hủy đăng ký đề tài theo mã số đăng ký (ma_dang_ky)
  cancel(id: number): Observable<void> {
    return this.http.delete<void>(`${this.endpoint}/${id}`);
  }
}
