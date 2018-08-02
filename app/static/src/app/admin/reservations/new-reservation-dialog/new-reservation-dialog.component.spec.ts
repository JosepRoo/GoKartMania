import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewReservationDialogComponent } from './new-reservation-dialog.component';

describe('NewReservationDialogComponent', () => {
  let component: NewReservationDialogComponent;
  let fixture: ComponentFixture<NewReservationDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewReservationDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewReservationDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
