import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Student } from '../models';

@Injectable({
  providedIn: 'root',
})
export class StudentApi {
  private readonly http = inject(HttpClient);
  // Địa chỉ API của SinhVien Service (chạy ở cổng 8001)
  private readonly endpoint = 'http://localhost:8001/api/v1/sinhviens';

  // Lấy danh sách toàn bộ sinh viên
  list(): Observable<Student[]> {
    return this.http.get<Student[]>(this.endpoint);
  }

  // Thêm mới một sinh viên
  create(student: Student): Observable<Student> {
    return this.http.post<Student>(this.endpoint, student);
  }

  // Cập nhật thông tin sinh viên theo mã số sinh viên
  update(student: Student): Observable<Student> {
    return this.http.put<Student>(`${this.endpoint}/${encodeURIComponent(student.ma_sinh_vien)}`, student);
  }

  // Xóa sinh viên theo mã số sinh viên
  delete(key: string): Observable<void> {
    return this.http.delete<void>(`${this.endpoint}/${encodeURIComponent(key)}`);
  }
}
