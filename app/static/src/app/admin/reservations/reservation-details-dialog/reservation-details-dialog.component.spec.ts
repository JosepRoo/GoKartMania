import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReservationDetailsDialogComponent } from './reservation-details-dialog.component';

describe('ReservationDetailsDialogComponent', () => {
  let component: ReservationDetailsDialogComponent;
  let fixture: ComponentFixture<ReservationDetailsDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ReservationDetailsDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReservationDetailsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
