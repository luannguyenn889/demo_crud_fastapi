import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Topic } from '../../models';

@Component({
  selector: 'app-topic-management',
  standalone: true,
  imports: [],
  templateUrl: './topic-management.html',
  styleUrl: './topic-management.css',
})
export class TopicManagement {
  @Input() topics: Topic[] = [];
  @Input() query = '';
  @Output() queryChange = new EventEmitter<string>();
  @Output() openAdd = new EventEmitter<void>();
  @Output() edit = new EventEmitter<Topic>();
  @Output() remove = new EventEmitter<Topic>();

  statusFilter: 'ALL' | 'MO_DANG_KY' | 'DA_DONG' = 'ALL';

  get filtered(): Topic[] {
    const q = this.query.trim().toLowerCase();
    return this.topics.filter((topic) => {
      const matchQuery = !q || `${topic.ma_de_tai} ${topic.ten_de_tai} ${topic.giang_vien_huong_dan ?? ''}`
        .toLowerCase()
        .includes(q);
      const matchStatus = this.statusFilter === 'ALL' || topic.trang_thai === this.statusFilter;
      return matchQuery && matchStatus;
    });
  }

  setStatusFilter(filter: 'ALL' | 'MO_DANG_KY' | 'DA_DONG'): void {
    this.statusFilter = filter;
  }
}
