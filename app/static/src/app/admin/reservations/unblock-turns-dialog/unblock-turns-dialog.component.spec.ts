import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UnblockTurnsDialogComponent } from './unblock-turns-dialog.component';

describe('UnblockTurnsDialogComponent', () => {
  let component: UnblockTurnsDialogComponent;
  let fixture: ComponentFixture<UnblockTurnsDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UnblockTurnsDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UnblockTurnsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
