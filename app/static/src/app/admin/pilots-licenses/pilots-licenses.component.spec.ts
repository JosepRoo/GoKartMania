import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PilotsLicensesComponent } from './pilots-licenses.component';

describe('PilotsLicensesComponent', () => {
  let component: PilotsLicensesComponent;
  let fixture: ComponentFixture<PilotsLicensesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PilotsLicensesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PilotsLicensesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
