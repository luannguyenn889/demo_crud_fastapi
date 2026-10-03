import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Student } from '../../models';

@Component({
  selector: 'app-student-management',
  standalone: true,
  imports: [],
  templateUrl: './student-management.html',
  styleUrl: './student-management.css',
})
export class StudentManagement {
  @Input() students: Student[] = [];
  @Input() query = '';
  @Output() queryChange = new EventEmitter<string>();
  @Output() openAdd = new EventEmitter<void>();
  @Output() edit = new EventEmitter<Student>();
  @Output() remove = new EventEmitter<Student>();

  get filtered(): Student[] {
    const q = this.query.trim().toLowerCase();
    if (!q) return this.students;
    return this.students.filter((student) =>
      `${student.ma_sinh_vien} ${student.ho_ten} ${student.email ?? ''} ${student.lop ?? ''} ${student.nganh ?? ''}`
        .toLowerCase()
        .includes(q)
    );
  }

  getInitials(name: string): string {
    if (!name) return 'SV';
    const parts = name.trim().split(/\s+/);
    if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }

  getAvatarClass(index: number): string {
    const classes = ['avatar-indigo', 'avatar-emerald', 'avatar-amber', 'avatar-rose', 'avatar-purple', 'avatar-teal'];
    return classes[index % classes.length];
  }
}
