import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { Navigation } from './components/navigation/navigation';
import { Overview } from './components/overview/overview';
import { RegistrationManagement } from './components/registration-management/registration-management';
import { StudentManagement } from './components/student-management/student-management';
import { TopicManagement } from './components/topic-management/topic-management';
import { Page, Registration, Student, Topic } from './models';
import { RegistrationApi } from './services/registration-api';
import { StudentApi } from './services/student-api';
import { TopicApi } from './services/topic-api';

export interface ToastItem {
  id: number;
  type: 'success' | 'error';
  title: string;
  message: string;
}

export interface ConfirmDialogData {
  title: string;
  message: string;
  confirmLabel: string;
  action: () => void;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    FormsModule,
    Navigation,
    Overview,
    StudentManagement,
    TopicManagement,
    RegistrationManagement,
  ],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  private readonly studentApi = inject(StudentApi);
  private readonly topicApi = inject(TopicApi);
  private readonly registrationApi = inject(RegistrationApi);

  tab = signal<Page>('overview');
  students = signal<Student[]>([]);
  topics = signal<Topic[]>([]);
  registrations = signal<Registration[]>([]);
  query = signal('');
  mobileMenuOpen = signal(false);

  // Forms & Modal states
  studentModalOpen = signal(false);
  topicModalOpen = signal(false);
  confirmModalOpen = signal(false);
  confirmData = signal<ConfirmDialogData | null>(null);

  studentForm: Student = this.emptyStudent();
  topicForm: Topic = this.emptyTopic();
  editingStudent = false;
  editingTopic = false;

  regStudent = '';
  regTopic = '';

  // Toasts
  toasts = signal<ToastItem[]>([]);
  private toastCounter = 0;

  ngOnInit(): void {
    this.refresh();
  }

  get pageLabel(): string {
    const labels: Record<Page, string> = {
      overview: 'Tổng quan hệ thống',
      students: 'Quản lý sinh viên',
      topics: 'Đề tài nghiên cứu',
      registrations: 'Đăng ký đồ án',
    };
    return labels[this.tab()];
  }

  private emptyStudent(): Student {
    return {
      ma_sinh_vien: '',
      ho_ten: '',
      email: null,
      lop: null,
      nganh: null,
      so_dien_thoai: null,
    };
  }

  private emptyTopic(): Topic {
    return {
      ma_de_tai: '',
      ten_de_tai: '',
      mo_ta: null,
      giang_vien_huong_dan: null,
      so_luong_toi_da: 1,
      trang_thai: 'MO_DANG_KY',
    };
  }

  // Navigation & Refresh
  open(page: Page): void {
    this.tab.set(page);
    this.mobileMenuOpen.set(false);
  }

  refresh(): void {
    this.studentApi.list().subscribe({
      next: (value) => this.students.set(value),
      error: (e) => this.fail('Không tải được danh sách sinh viên', e),
    });
    this.topicApi.list().subscribe({
      next: (value) => this.topics.set(value),
      error: (e) => this.fail('Không tải được danh sách đề tài', e),
    });
    this.registrationApi.list().subscribe({
      next: (value) => this.registrations.set(value),
      error: (e) => this.fail('Không tải được danh sách đăng ký', e),
    });
  }

  // Toast System
  addToast(type: 'success' | 'error', title: string, message: string): void {
    const id = ++this.toastCounter;
    const newToast: ToastItem = { id, type, title, message };
    this.toasts.update((current) => [...current, newToast]);

    setTimeout(() => {
      this.removeToast(id);
    }, 4000);
  }

  removeToast(id: number): void {
    this.toasts.update((current) => current.filter((t) => t.id !== id));
  }

  private fail(defaultTitle: string, error: HttpErrorResponse): void {
    const detail =
      error.status === 0
        ? 'Không kết nối được dịch vụ backend (vui lòng kiểm tra API).'
        : error.error?.detail || error.message || 'Yêu cầu không thành công.';
    this.addToast('error', defaultTitle, detail);
  }

  // Student Operations
  openAddStudent(): void {
    this.studentForm = this.emptyStudent();
    this.editingStudent = false;
    this.studentModalOpen.set(true);
  }

  editStudent(item: Student): void {
    this.studentForm = { ...item };
    this.editingStudent = true;
    this.studentModalOpen.set(true);
  }

  closeStudentModal(): void {
    this.studentModalOpen.set(false);
  }

  saveStudent(): void {
    const request = this.editingStudent
      ? this.studentApi.update(this.studentForm)
      : this.studentApi.create(this.studentForm);

    request.subscribe({
      next: () => {
        this.closeStudentModal();
        this.addToast(
          'success',
          'Thành công',
          this.editingStudent
            ? `Đã cập nhật hồ sơ sinh viên ${this.studentForm.ma_sinh_vien}`
            : `Đã thêm sinh viên ${this.studentForm.ho_ten} (${this.studentForm.ma_sinh_vien})`
        );
        this.refresh();
      },
      error: (e) => this.fail('Lưu sinh viên thất bại', e),
    });
  }

  confirmDeleteStudent(item: Student): void {
    this.confirmData.set({
      title: 'Xóa hồ sơ sinh viên',
      message: `Bạn có chắc chắn muốn xóa sinh viên "${item.ho_ten}" (Mã: ${item.ma_sinh_vien})? Hành động này không thể hoàn tác.`,
      confirmLabel: 'Xác nhận xóa',
      action: () => {
        this.studentApi.delete(item.ma_sinh_vien).subscribe({
          next: () => {
            this.confirmModalOpen.set(false);
            this.addToast('success', 'Đã xóa sinh viên', `Đã xóa sinh viên ${item.ma_sinh_vien}`);
            this.refresh();
          },
          error: (e) => this.fail('Xóa sinh viên thất bại', e),
        });
      },
    });
    this.confirmModalOpen.set(true);
  }

  // Topic Operations
  openAddTopic(): void {
    this.topicForm = this.emptyTopic();
    this.editingTopic = false;
    this.topicModalOpen.set(true);
  }

  editTopic(item: Topic): void {
    this.topicForm = { ...item };
    this.editingTopic = true;
    this.topicModalOpen.set(true);
  }

  closeTopicModal(): void {
    this.topicModalOpen.set(false);
  }

  saveTopic(): void {
    const request = this.editingTopic
      ? this.topicApi.update(this.topicForm)
      : this.topicApi.create(this.topicForm);

    request.subscribe({
      next: () => {
        this.closeTopicModal();
        this.addToast(
          'success',
          'Thành công',
          this.editingTopic
            ? `Đã cập nhật đề tài ${this.topicForm.ma_de_tai}`
            : `Đã tạo đề tài mới ${this.topicForm.ten_de_tai}`
        );
        this.refresh();
      },
      error: (e) => this.fail('Lưu đề tài thất bại', e),
    });
  }

  confirmDeleteTopic(item: Topic): void {
    this.confirmData.set({
      title: 'Xóa đề tài nghiên cứu',
      message: `Bạn có chắc chắn muốn xóa đề tài "${item.ten_de_tai}" (Mã: ${item.ma_de_tai})? Mọi dữ liệu liên quan sẽ bị ảnh hưởng.`,
      confirmLabel: 'Xác nhận xóa',
      action: () => {
        this.topicApi.delete(item.ma_de_tai).subscribe({
          next: () => {
            this.confirmModalOpen.set(false);
            this.addToast('success', 'Đã xóa đề tài', `Đã xóa đề tài ${item.ma_de_tai}`);
            this.refresh();
          },
          error: (e) => this.fail('Xóa đề tài thất bại', e),
        });
      },
    });
    this.confirmModalOpen.set(true);
  }

  // Registration Operations
  createRegistration(): void {
    if (!this.regStudent || !this.regTopic) {
      this.addToast('error', 'Lỗi nhập liệu', 'Vui lòng chọn đầy đủ sinh viên và đề tài.');
      return;
    }

    this.registrationApi
      .create({ ma_sinh_vien: this.regStudent, ma_de_tai: this.regTopic })
      .subscribe({
        next: (created) => {
          this.regStudent = '';
          this.regTopic = '';
          this.addToast(
            'success',
            'Đăng ký thành công',
            `Đã ghi nhận lượt đăng ký #${created.ma_dang_ky} cho sinh viên ${created.ma_sinh_vien}`
          );
          this.refresh();
        },
        error: (e) => this.fail('Đăng ký đề tài thất bại', e),
      });
  }

  confirmCancelRegistration(item: Registration): void {
    this.confirmData.set({
      title: 'Hủy đăng ký đề tài',
      message: `Bạn có chắc chắn muốn hủy lượt đăng ký #${item.ma_dang_ky} của sinh viên ${item.ma_sinh_vien}?`,
      confirmLabel: 'Xác nhận hủy',
      action: () => {
        this.registrationApi.cancel(item.ma_dang_ky).subscribe({
          next: () => {
            this.confirmModalOpen.set(false);
            this.addToast('success', 'Đã hủy đăng ký', `Đã hủy lượt đăng ký #${item.ma_dang_ky}`);
            this.refresh();
          },
          error: (e) => this.fail('Hủy đăng ký thất bại', e),
        });
      },
    });
    this.confirmModalOpen.set(true);
  }
}
