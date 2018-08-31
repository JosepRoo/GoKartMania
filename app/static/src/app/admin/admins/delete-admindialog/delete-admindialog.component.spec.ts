import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteAdmindialogComponent } from './delete-admindialog.component';

describe('DeleteAdmindialogComponent', () => {
  let component: DeleteAdmindialogComponent;
  let fixture: ComponentFixture<DeleteAdmindialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeleteAdmindialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeleteAdmindialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
