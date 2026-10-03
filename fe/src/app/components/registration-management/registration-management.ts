import { DatePipe } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Registration, Student, Topic } from '../../models';

@Component({
  selector: 'app-registration-management',
  standalone: true,
  imports: [FormsModule, DatePipe],
  templateUrl: './registration-management.html',
  styleUrl: './registration-management.css',
})
export class RegistrationManagement {
  @Input() students: Student[] = [];
  @Input() topics: Topic[] = [];
  @Input() registrations: Registration[] = [];
  @Input() studentKey = '';
  @Output() studentKeyChange = new EventEmitter<string>();
  @Input() topicKey = '';
  @Output() topicKeyChange = new EventEmitter<string>();
  @Output() create = new EventEmitter<void>();
  @Output() cancel = new EventEmitter<Registration>();

  statusFilter: 'ALL' | 'DA_DANG_KY' | 'DA_HUY' = 'ALL';
  regQuery = '';

  get filteredRegistrations(): Registration[] {
    const q = this.regQuery.trim().toLowerCase();
    return this.registrations.filter((r) => {
      const student = this.getStudent(r.ma_sinh_vien);
      const topic = this.getTopic(r.ma_de_tai);
      const searchTarget = `${r.ma_dang_ky} ${r.ma_sinh_vien} ${student?.ho_ten ?? ''} ${r.ma_de_tai} ${topic?.ten_de_tai ?? ''}`.toLowerCase();
      const matchQuery = !q || searchTarget.includes(q);
      const matchStatus = this.statusFilter === 'ALL' || r.trang_thai === this.statusFilter;
      return matchQuery && matchStatus;
    });
  }

  get selectedTopic(): Topic | undefined {
    return this.topics.find((t) => t.ma_de_tai === this.topicKey);
  }

  get selectedStudent(): Student | undefined {
    return this.students.find((s) => s.ma_sinh_vien === this.studentKey);
  }

  getTopicActiveCount(ma_de_tai: string): number {
    return this.registrations.filter((r) => r.ma_de_tai === ma_de_tai && r.trang_thai === 'DA_DANG_KY').length;
  }

  getStudent(ma_sinh_vien: string): Student | undefined {
    return this.students.find((s) => s.ma_sinh_vien === ma_sinh_vien);
  }

  getTopic(ma_de_tai: string): Topic | undefined {
    return this.topics.find((t) => t.ma_de_tai === ma_de_tai);
  }
}
