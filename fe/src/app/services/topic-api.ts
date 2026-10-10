import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Topic } from '../models';

@Injectable({
  providedIn: 'root',
})
export class TopicApi {
  private readonly http = inject(HttpClient);
  // Địa chỉ API của DeTai Service (chạy ở cổng 8002)
  private readonly endpoint = 'http://localhost:8002/api/v1/detais';

  // Lấy danh sách toàn bộ đề tài tốt nghiệp
  list(): Observable<Topic[]> {
    return this.http.get<Topic[]>(this.endpoint);
  }

  // Thêm mới một đề tài tốt nghiệp
  create(topic: Topic): Observable<Topic> {
    return this.http.post<Topic>(this.endpoint, topic);
  }

  // Cập nhật thông tin đề tài theo mã đề tài
  update(topic: Topic): Observable<Topic> {
    return this.http.put<Topic>(`${this.endpoint}/${encodeURIComponent(topic.ma_de_tai)}`, topic);
  }

  // Xóa đề tài theo mã đề tài
  delete(key: string): Observable<void> {
    return this.http.delete<void>(`${this.endpoint}/${encodeURIComponent(key)}`);
  }
}
