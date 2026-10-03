import { Component, Input, Output, EventEmitter } from '@angular/core';
import { DatePipe } from '@angular/common';
import { Registration, Student, Topic, Page } from '../../models';

@Component({
  selector: 'app-overview',
  standalone: true,
  imports: [DatePipe],
  templateUrl: './overview.html',
  styleUrl: './overview.css',
})
export class Overview {
  @Input() students: Student[] = [];
  @Input() topics: Topic[] = [];
  @Input() registrations: Registration[] = [];
  @Output() navigate = new EventEmitter<Page>();

  get openTopics(): number {
    return this.topics.filter((topic) => topic.trang_thai === 'MO_DANG_KY').length;
  }

  get closedTopics(): number {
    return this.topics.filter((topic) => topic.trang_thai === 'DA_DONG').length;
  }

  get activeRegistrations(): number {
    return this.registrations.filter((item) => item.trang_thai === 'DA_DANG_KY').length;
  }

  get cancelledRegistrations(): number {
    return this.registrations.filter((item) => item.trang_thai === 'DA_HUY').length;
  }

  get totalCapacity(): number {
    return this.topics.reduce((acc, t) => acc + (t.so_luong_toi_da || 1), 0);
  }

  get fillRate(): number {
    if (!this.totalCapacity) return 0;
    const rate = Math.round((this.activeRegistrations / this.totalCapacity) * 100);
    return Math.min(rate, 100);
  }

  getStudentName(studentKey: string): string {
    const student = this.students.find((s) => s.ma_sinh_vien === studentKey);
    return student ? student.ho_ten : studentKey;
  }

  getTopicName(topicKey: string): string {
    const topic = this.topics.find((t) => t.ma_de_tai === topicKey);
    return topic ? topic.ten_de_tai : topicKey;
  }
}
