import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewPromoDialogComponent } from './new-promo-dialog.component';

describe('NewPromoDialogComponent', () => {
  let component: NewPromoDialogComponent;
  let fixture: ComponentFixture<NewPromoDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewPromoDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewPromoDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
