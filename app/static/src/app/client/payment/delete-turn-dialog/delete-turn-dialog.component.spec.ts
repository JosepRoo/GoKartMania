import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteTurnDialogComponent } from './delete-turn-dialog.component';

describe('DeleteTurnDialogComponent', () => {
  let component: DeleteTurnDialogComponent;
  let fixture: ComponentFixture<DeleteTurnDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeleteTurnDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeleteTurnDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
