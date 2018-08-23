import {
  Component,
  OnInit,
  ElementRef,
  ViewChild,
  Input,
  Output,
  EventEmitter
} from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl, FormArray } from '@angular/forms';

// Services
import { ReservationService } from '../services/reservation.service';
import { PilotService } from '../services/pilot.service';

@Component({
  selector: 'app-pilots',
  templateUrl: './pilots.component.html',
  styleUrls: ['./pilots.component.scss']
})
export class PilotsComponent implements OnInit {
  reservation: FormGroup;
  minBirthDayDate = new Date(1920, 1, 1);
  maxBirthDayDate = new Date();
  numbers: Array<Number>;
  loading: Boolean = false;
  error = {
    show: false,
    text: ''
  };
  @Input() groupType;
  @Output() pilotsSelected: EventEmitter<any> = new EventEmitter<any>();

  @ViewChild('pilotFormButton') pilotFormButton: ElementRef;

  constructor(
    private formBuilder: FormBuilder,
    private reservationService: ReservationService,
    private pilotService: PilotService
  ) {
    this.numbers = Array(8)
      .fill(0)
      .map((x, i) => i);
  }

  ngOnInit() {
    this.reservation = this.formBuilder.group({
      id_location: [1, Validators.required],
      type: ['', Validators.required],
      pilots: this.formBuilder.array([]),
      _id: []
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
    const wasLicensed = pilot.controls.buy_license.value;
    pilots.controls[index] = this.createPilot(0);
    pilot = pilots.controls[index] as FormGroup;
    pilot.controls.name.setValue(name);
  }

  buyLicense(index) {
    const pilots = this.reservation.get('pilots') as FormArray;
    let pilot = pilots.controls[index] as FormGroup;
    const name = pilot.controls.name.value;
    const wasLicensed = pilot.controls.licensed.value;
    pilots.controls[index] = this.createPilot(1);
    pilot = pilots.controls[index] as FormGroup;
    pilot.controls.name.setValue(name);
  }

  // create pilot form
  createPilot(isLicense) {
    if (isLicense) {
      return this.formBuilder.group({
        name: [null, Validators.required],
        last_name: [null, Validators.required],
        email: [null, [Validators.required, Validators.email]],
        birth_date: [null, [Validators.required]],
        postal_code: [
          null,
          [Validators.required, Validators.pattern('[0-9]{5}')]
        ],
        nickname: [null, Validators.required],
        city: [null, Validators.required],
        licensed: [true],
        buy_license: [false],
        location: ['Carso']
      });
    }
    return this.formBuilder.group({
      name: [null, Validators.required],
      last_name: [null],
      birth_date: [null],
      email: [null],
      postal_code: [null],
      nickname: [null],
      city: [null],
      licensed: [false],
      buy_license: [true],
      location: ['Carso']
    });
  }

  // add one pilot form to the array
  addPilot() {
    const pilots = this.reservation.get('pilots') as FormArray;
    if (pilots.length < 8 && this.reservation.controls.type.value) {
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
    const ar = this.reservation.get('pilots') as FormArray;
    const len = ar.length;
    if (self.reservation.valid && len) {
      this.loading = true;
      this.error = { show: false, text: '' };
      this.reservation.setValue(this.reservation.getRawValue());
      if (this.validateAge()) {
        const reservationData = self.reservation.getRawValue();
        self.reservationService.addReservation(reservationData).subscribe(
          res => {
            self.pilotService
              .addPilots(self.reservation.getRawValue().pilots)
              .subscribe(
                // tslint:disable-next-line:no-shadowed-variable
                res => {
                  const data = self.reservation.getRawValue();
                  data.pilots = res;
                  self.pilotsSelected.emit(data);
                },
                error => {
                  this.error = { show: true, text: error };
                  this.loading = false;
                }
              );
          },
          error => {
            this.error = { show: true, text: error };
            this.loading = false;
          }
        );
      } else {
        this.error = {
          show: true,
          text:
            'Alguno de tus pilotos no cumple con la edad necesaria para este grupo.'
        };
        this.loading = false;
      }
    }
  }

  validateAge() {
    const pilots = this.reservation.get('pilots') as FormArray;
    const res = true;
    for (let i = 0; i < pilots.controls.length; i++) {
      const pilot = pilots.controls[i] as FormGroup;
      if (pilot.controls.buy_license.value || pilot.controls.licensed.value) {
        const timeDiff = Math.abs(Date.now() - pilot.controls.birth_date.value);
        const age = Math.floor(timeDiff / (1000 * 3600 * 24) / 365);
        if (
          (this.reservation.controls.type.value === 'Niños' &&
            (age < 5 || age > 12)) ||
          (this.reservation.controls.type.value === 'Adultos' && age < 12)
        ) {
          return false;
        }
      }
    }
    return res;
  }

  //  submit reservation form
  submitPilotsForm() {
    this.pilotFormButton.nativeElement.click();
  }
}
