import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl, FormArray } from '@angular/forms';

// Services
import { ReservationService } from '../services/reservation.service';
import { PilotService } from '../services/pilot.service';

@Component({
  selector: 'app-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.scss']
})
export class ReservationComponent implements OnInit {
  reservation: FormGroup;
  minBirthDayDate = new Date(1920, 1, 1);
  maxBirthDayDate = new Date();
  numbers: Array<Number>;

  @ViewChild('pilotFormButton') pilotFormButton: ElementRef;

  constructor(
    private formBuilder: FormBuilder,
    private reservationService: ReservationService,
    private pilotService: PilotService
  ) {
    this.numbers = Array(7)
      .fill(0)
      .map((x, i) => i);
  }

  ngOnInit() {
    this.reservation = this.formBuilder.group({
      id_location: [1, Validators.required],
      type: ['', Validators.required],
      pilots: this.formBuilder.array([this.createPilot(0)])
    });
  }

  getFormData() {
    return this.reservation.get('pilots') as FormGroup;
  }

  // change the pilot send to a one that needs license data
  changePilotLicense(index) {
    const pilots = this.reservation.get('pilots') as FormArray;
    let pilot = pilots.controls[index] as FormGroup;
    const name = pilot.controls.name.value;
    if (!pilot.controls.licensed.value) {
      pilots.controls[index] = this.createPilot(0);
    }
    // tslint:disable-next-line:one-line
    else {
      pilots.controls[index] = this.createPilot(1);
    }
    pilot = pilots.controls[index] as FormGroup;
    pilot.controls.name.setValue(name);
  }

  // create pilot form
  createPilot(isLicense) {
    if (isLicense) {
      return this.formBuilder.group({
        name: ['', Validators.required],
        lastName: ['', Validators.required],
        email: ['', [Validators.required, Validators.email]],
        birthDate: ['', Validators.required],
        postalCode: ['', [Validators.required, Validators.pattern('[0-9]{5}')]],
        nickName: ['', Validators.required],
        city: ['', Validators.required],
        licensed: [true]
      });
    }
    return this.formBuilder.group({
      name: ['', Validators.required],
      lastName: [''],
      birthDate: [''],
      email: [''],
      postalCode: [''],
      nickName: [''],
      city: [''],
      licensed: [false]
    });
  }

  // add one pilot form to the array
  addPilot() {
    const pilots = this.reservation.get('pilots') as FormArray;
    if (pilots.length < 8) {
      pilots.push(this.createPilot(0));
      this.numbers.splice(0, 1);
    }
  }

  // remove pilot form to the array
  removePilot(index) {
    const pilots = this.reservation.get('pilots') as FormArray;
    pilots.removeAt(index);
    this.numbers.push(1);
  }

  // calls the service to add the reservation
  sendPilots() {
    const self = this;
    if (self.reservation.valid) {
      const reservationData = self.reservation.getRawValue();
      self.reservationService.addReservation(reservationData).subscribe(
        () => {
        self.pilotService.addPilots(self.reservation.getRawValue().pilots).subscribe(
          res => {
          console.log(res);
          }, error => {
            console.log(error);
          }, () => { });
      }, error => {
        console.log(error);
      }, () => {});
    }
  }

  //  submit reservation form
  submitPilotsForm() {
    this.pilotFormButton.nativeElement.click();
  }
}
