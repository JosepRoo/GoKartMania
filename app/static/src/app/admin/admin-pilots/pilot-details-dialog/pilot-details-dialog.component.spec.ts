import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PilotDetailsDialogComponent } from './pilot-details-dialog.component';

describe('PilotDetailsDialogComponent', () => {
  let component: PilotDetailsDialogComponent;
  let fixture: ComponentFixture<PilotDetailsDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PilotDetailsDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PilotDetailsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
