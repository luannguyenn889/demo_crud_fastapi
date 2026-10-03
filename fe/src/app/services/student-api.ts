import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Student } from '../models';

@Injectable({
  providedIn: 'root',
})
export class StudentApi {
  private readonly http = inject(HttpClient);
  private readonly endpoint = 'http://localhost:8001/api/v1/sinhviens';

  list(): Observable<Student[]> {
    return this.http.get<Student[]>(this.endpoint);
  }

  create(student: Student): Observable<Student> {
    return this.http.post<Student>(this.endpoint, student);
  }

  update(student: Student): Observable<Student> {
    return this.http.put<Student>(`${this.endpoint}/${encodeURIComponent(student.ma_sinh_vien)}`, student);
  }

  delete(key: string): Observable<void> {
    return this.http.delete<void>(`${this.endpoint}/${encodeURIComponent(key)}`);
  }
}
