import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Page } from '../../models';

@Component({
  selector: 'app-navigation',
  standalone: true,
  templateUrl: './navigation.html',
  styleUrl: './navigation.css',
})
export class Navigation {
  @Input({ required: true }) page!: Page;
  @Input() mobileOpen = false;
  @Output() navigate = new EventEmitter<Page>();
  @Output() closeMobile = new EventEmitter<void>();

  onSelect(target: Page): void {
    this.navigate.emit(target);
    this.closeMobile.emit();
  }
}
