import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BlockTurnsDialogComponent } from './block-turns-dialog.component';

describe('BlockTurnsDialogComponent', () => {
  let component: BlockTurnsDialogComponent;
  let fixture: ComponentFixture<BlockTurnsDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BlockTurnsDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BlockTurnsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
