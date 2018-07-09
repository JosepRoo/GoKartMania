import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit, ViewChild, Input, EventEmitter, Output } from '@angular/core';
import { DatePipe } from '@angular/common';
import 'rxjs/add/operator/map';

// services
import { DatesService } from './../services/dates.service';
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
  preventBack: Boolean = true;
  showLoading: Boolean = false;
  selectedDay: Date;
  turn: FormGroup;
  @Output() goBack: EventEmitter<any> = new EventEmitter<any>();
  @ViewChild(CalendarComponent) calendar: CalendarComponent;
  @Input() reservation: any;

  constructor(private datesService: DatesService, private datePipe: DatePipe, private formBuilder: FormBuilder) {}

  ngOnInit() {
    const now = new Date();
    this.setDateRange(now.getFullYear(), now.getMonth(), now.getDate());
    this.getAvailableDates();
    this.turn = this.formBuilder.group({
      date: ['', Validators.required],
      schedule: ['', Validators.required],
      turn_number: ['', Validators.required]
    });
  }

  // event emitted when calendar component detects a click on a day
  onSelectedDate(date) {
    if (this.findDay(date)) {
      this.selectedDay = date;
      this.turn.controls.date.setValue(this.datePipe.transform(date, 'yyyy-MM-dd'));
      this.datesService.getAvailableSchedules(this.turn.controls.date.value).subscribe(res => {
        this.availableSchedules = res;
        console.log(res);
      })
    }

  }

  // calls service for available days
  getAvailableDates() {
    this.datesService
      .getAvailableDates(
        this.datePipe.transform(this.startDate, 'yyyy-MM-dd'),
        this.datePipe.transform(this.endDate, 'yyyy-MM-dd')
      )
      .subscribe((res: Array<any>) => {
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
      }, error => {
        console.log(error);
      });
  }

  // set the new start and end dates
  setDateRange(year, month, day) {
    const date = new Date(year, month, day);
    const daysMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0);
    this.startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    this.endDate = new Date(
      date.getFullYear(),
      date.getMonth(),
      daysMonth.getDate()
    );
  }

  // emitted when calendar detects a month change by user click
  onDateChange(date: Date) {
    const now = new Date();
    this.preventBack = now.getFullYear() === date.getFullYear() && now.getMonth() === date.getMonth();
    this.setDateRange(date.getFullYear(), date.getMonth(), date.getDate());
    this.availableDates = null;
    this.getAvailableDates();
  }

  findDay(date) {
    if (this.availableDates) {
      return this.availableDates.find(el => el.fecha.toISOString().split('T')[0] === date.toISOString().split('T')[0] && el.cupo !== 0);
    }
  }
}
