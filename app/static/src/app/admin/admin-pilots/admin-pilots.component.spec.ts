import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminPilotsComponent } from './admin-pilots.component';

describe('AdminPilotsComponent', () => {
  let component: AdminPilotsComponent;
  let fixture: ComponentFixture<AdminPilotsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdminPilotsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminPilotsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
