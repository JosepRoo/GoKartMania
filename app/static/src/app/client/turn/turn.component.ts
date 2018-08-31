import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit, ViewChild, Input, EventEmitter, Output, ElementRef } from '@angular/core';
import { DatePipe } from '@angular/common';
import 'rxjs/add/operator/map';

// services
import { DatesService } from '../services/dates.service';
import { CalendarComponent } from '../calendar/calendar.component';

@Component({
  selector: 'app-turn',
  templateUrl: './turn.component.html',
  styleUrls: ['./turn.component.scss']
})
export class TurnComponent implements OnInit {
  startDate: Date;
  endDate: Date;
  availableDates: Array<any>;
  availableSchedules: Array<any>;
  availableTurns: Array<any>;
  availablePositions: Array<any>;
  preventBack: Boolean = true;
  showLoading: Boolean = false;
  selectedDay: Date;
  turn: FormGroup;
  alreadyDate = false;
  pilotId = 0;
  @Output() goBack: EventEmitter<any> = new EventEmitter<any>();
  @Output() reservationOutput: EventEmitter<any> = new EventEmitter<any>();
  @ViewChild(CalendarComponent) calendar: CalendarComponent;
  @Input() reservation: any;
  @ViewChild('formButton') formButton: ElementRef;
  error = {
    show: false,
    text: ''
  };
  pilot;
  positions;
  mode = "normal";

  constructor(
    private datesService: DatesService,
    private datePipe: DatePipe,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit() {
    const now = new Date();
    this.setDateRange(now.getFullYear(), now.getMonth(), now.getDate());
    this.getAvailableDates();
    this.turn = this.formBuilder.group({
      date: ['', Validators.required],
      schedule: ['', Validators.required],
      turn_number: ['', Validators.required],
      positions: [{}, Validators.required]
    });
    if (this.reservation.date) {
      this.turn.controls.date.setValue(this.reservation.date);
      this.onSelectedDate(this.reservation.date, 1);
      this.alreadyDate = true;
    }
  }

  // event emitted when calendar component detects a click on a day
  onSelectedDate(date, flag) {
    if (this.findDay(date) || flag) {
      this.selectedDay = date;
      this.turn.controls.date.setValue(
        this.datePipe.transform(date, 'yyyy-MM-dd')
      );
      this.datesService
        .getAvailableSchedules(this.turn.controls.date.value)
        .subscribe(res => {
          res = res.filter(sch => {
            if (sch.cupo !== 0) {
              return sch;
            }
          });
          this.availableSchedules = res;
        });
    }
    this.turn.controls.schedule.setValue(null);
    this.turn.controls.turn_number.setValue(null);
    this.availablePositions = [];
  }
 
  // calls service for available days
  getAvailableDates() {
    this.datesService
      .getAvailableDates(
        this.datePipe.transform(this.startDate, 'yyyy-MM-dd'),
        this.datePipe.transform(this.endDate, 'yyyy-MM-dd')
      )
      .subscribe(
        (res: Array<any>) => {
          res.map(
            el => {
              el.fecha = new Date(el.fecha);
            },
            error => {
              {
              }
            }
          );
          this.availableDates = res;
        }
      );
  }

  // set the new start and end dates
  setDateRange(year, month, day) {
    const date = new Date(year, month, day);
    const daysMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0);
    this.startDate = new Date(
      date.getFullYear(),
      date.getMonth(),
      date.getDate()
    );
    this.endDate = new Date(
      date.getFullYear(),
      date.getMonth(),
      daysMonth.getDate()
    );
  }

  // emitted when calendar detects a month change by user click
  onDateChange(date: Date) {
    const now = new Date();
    this.preventBack =
      now.getFullYear() === date.getFullYear() &&
      now.getMonth() === date.getMonth();
    this.setDateRange(date.getFullYear(), date.getMonth(), date.getDate());
    this.availableDates = null;
    this.getAvailableDates();
    this.error.show = false;
  }

  findDay(date) {
    if (this.availableDates) {
      return this.availableDates.find(
        el =>
          el.fecha.toISOString().split('T')[0] ===
            date.toISOString().split('T')[0] && el.cupo !== 0
      );
    }
  }

  assignTurn(schedule) {
    schedule = schedule.turns.filter(turn => {
      if (turn.status !== 0) {
        return turn;
      }
    });
    this.availableTurns = schedule;
    this.turn.controls.turn_number.setValue(null);
    this.availablePositions = [];
    this.error.show = false;
  }

  getHour() {
    return this.turn.controls.schedule.value;
  }

  assignPositions(turn) {
    turn.positions = turn.positions.filter(el => {
      if (el.status !== 0) {
        el.clicked = false;
        return el;
      }
    });
    this.availablePositions = turn.positions;
    this.turn.controls.positions.setValue({});
    this.pilotId = 0;
    this.pilot = this.reservation.pilots[this.pilotId].nickname;
    this.positions = Object.keys(this.turn.controls.positions.value);
    this.error.show = false;
  }

  selectPosition(position) {
    if (!position.clicked) {
      if (
        Number(this.reservation.pilots.length) >
        Number(Object.keys(this.turn.controls.positions.value).length)
      ) {
        position.clicked = !position.clicked;
        const positions = this.turn.controls.positions.value;
        positions['pos' + position.position] = this.reservation.pilots[
          this.pilotId
        ]._id;
        this.availablePositions.find(x=> x.position==position.position).pilot = this.reservation.pilots[this.pilotId].nickname;
        if (
          Number(this.reservation.pilots.length) >
          Number(Object.keys(this.turn.controls.positions.value).length)
        ) {
          while(Object.values(this.turn.controls.positions.value).includes(this.reservation.pilots[this.pilotId]._id)){
            this.pilotId = this.pilotId + 1;
          }
        }
        this.pilot = this.reservation.pilots[this.pilotId].nickname;
        this.turn.controls.positions.setValue(positions);
        this.positions = Object.keys(this.turn.controls.positions.value);
      }
    } else {
      position.clicked = !position.clicked;
      const positions = this.turn.controls.positions.value;
      delete positions['pos' + position.position];
      this.availablePositions.find(x=> x.position==position.position).pilot = null;
      this.pilotId = 0;
      while(Object.values(this.turn.controls.positions.value).includes(this.reservation.pilots[this.pilotId]._id)){
        this.pilotId = this.pilotId + 1;
      }
      this.pilot = this.reservation.pilots[this.pilotId].nickname;
      this.turn.controls.positions.setValue(positions);
      this.positions = Object.keys(this.turn.controls.positions.value);
    }
    this.error.show = false;
  }

  // submitSendTurn() {
  //   this.formButton.nativeElement.click();
  // }

  sendTurn() {
    this.error.show = false;
    if (!this.turn.valid) {
      this.error.show = true;
      this.error.text =
        'Debes seleccionar todos los campos para completar tu reservación';
    } else {
      if (
        Object.keys(this.turn.controls.positions.value).length >=
        this.reservation.pilots.length
      ) {
        this.datesService.createTurn(this.turn.getRawValue()).subscribe(
          res => {
            res.date = this.turn.controls.date.value;
            res.turn_id = res._id;
            delete res._id;
            this.reservationOutput.emit({...this.reservation, ...res});
          },
          error => {
            this.error.show = true;
            this.error.text = error;
          }
        );
      } else {
        this.error.show = true;
        this.error.text =
          'Aun no seleccionas todos los gokarts de tu reservación';
      }
    }
  }
}
