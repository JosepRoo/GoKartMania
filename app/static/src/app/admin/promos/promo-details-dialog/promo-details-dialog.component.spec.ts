import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PromoDetailsDialogComponent } from './promo-details-dialog.component';

describe('PromoDetailsDialogComponent', () => {
  let component: PromoDetailsDialogComponent;
  let fixture: ComponentFixture<PromoDetailsDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PromoDetailsDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PromoDetailsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
