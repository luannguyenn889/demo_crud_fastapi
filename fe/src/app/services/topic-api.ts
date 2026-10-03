import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Topic } from '../models';

@Injectable({
  providedIn: 'root',
})
export class TopicApi {
  private readonly http = inject(HttpClient);
  private readonly endpoint = 'http://localhost:8002/api/v1/detais';

  list(): Observable<Topic[]> {
    return this.http.get<Topic[]>(this.endpoint);
  }

  create(topic: Topic): Observable<Topic> {
    return this.http.post<Topic>(this.endpoint, topic);
  }

  update(topic: Topic): Observable<Topic> {
    return this.http.put<Topic>(`${this.endpoint}/${encodeURIComponent(topic.ma_de_tai)}`, topic);
  }

  delete(key: string): Observable<void> {
    return this.http.delete<void>(`${this.endpoint}/${encodeURIComponent(key)}`);
  }
}
