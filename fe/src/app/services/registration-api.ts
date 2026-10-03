import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Registration } from '../models';

export type RegistrationInput = {
  ma_sinh_vien: string;
  ma_de_tai: string;
};

@Injectable({
  providedIn: 'root',
})
export class RegistrationApi {
  private readonly http = inject(HttpClient);
  private readonly endpoint = 'http://localhost:8003/api/v1/dang-ky';

  list(): Observable<Registration[]> {
    return this.http.get<Registration[]>(this.endpoint);
  }

  create(input: RegistrationInput): Observable<Registration> {
    return this.http.post<Registration>(this.endpoint, input);
  }

  cancel(id: number): Observable<void> {
    return this.http.delete<void>(`${this.endpoint}/${id}`);
  }
}
