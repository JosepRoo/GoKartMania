import {
  Component,
  ChangeDetectionStrategy,
  OnInit,
  ViewEncapsulation,
  Output,
  EventEmitter,
  Input
} from '@angular/core';
import {
  subMonths,
  addMonths,
  addDays,
  addWeeks,
  subDays,
  subWeeks,
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
  startOfDay,
  endOfDay
} from 'date-fns';
import { CalendarEvent, CalendarMonthViewDay } from 'angular-calendar';
import { DayViewHour } from 'calendar-utils';

type CalendarPeriod = 'day' | 'week' | 'month';

function addPeriod(period: CalendarPeriod, date: Date, amount: number): Date {
  return {
    day: addDays,
    week: addWeeks,
    month: addMonths
  }[period](date, amount);
}

function subPeriod(period: CalendarPeriod, date: Date, amount: number): Date {
  return {
    day: subDays,
    week: subWeeks,
    month: subMonths
  }[period](date, amount);
}

function startOfPeriod(period: CalendarPeriod, date: Date): Date {
  return {
    day: startOfDay,
    week: startOfWeek,
    month: startOfMonth
  }[period](date);
}

function endOfPeriod(period: CalendarPeriod, date: Date): Date {
  return {
    day: endOfDay,
    week: endOfWeek,
    month: endOfMonth
  }[period](date);
}

@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  encapsulation: ViewEncapsulation.None,
  styleUrls: ['./calendar.component.scss']
})
export class CalendarComponent implements OnInit {
  view: CalendarPeriod = 'month';
  viewDate: Date = new Date();
  @Input() date: Date;
  events: CalendarEvent[] = [];
  clickedDate: Date;
  selectedMonthViewDay: CalendarMonthViewDay;
  selectedDayViewDate: Date;
  dayView: DayViewHour[];
  minDate: Date = new Date();
  maxDate: Date = addMonths(new Date(), 2);
  monthLimit;
  @Input() prevBtnDisabled: Boolean;
  nextBtnDisabled: Boolean = false;
  // tslint:disable-next-line:no-output-on-prefix
  @Output() onSelectedDate: EventEmitter<any> = new EventEmitter<any>();
  // tslint:disable-next-line:no-output-on-prefix
  @Output() onDateChange: EventEmitter<any> = new EventEmitter<any>();
  @Input() availableDates: Array<any>;

  constructor() {
    this.dateOrViewChanged();
  }

  ngOnInit() {
    this.viewDate = new Date(this.date.getFullYear(), this.date.getMonth(), 1);
    this.monthLimit = false;
  }

  increment(): void {
    this.changeDate(addPeriod(this.view, this.viewDate, 0));
  }

  decrement(): void {
    this.changeDate(subPeriod(this.view, this.viewDate, 1));
  }

  today(): void {
    this.changeDate(new Date());
  }

  dateIsValid(date: Date): boolean {
    return date >= this.minDate && date <= this.maxDate;
  }

  changeDate(date: Date): void {
    this.viewDate = date;
    this.dateOrViewChanged();
  }

  changeView(view: CalendarPeriod): void {
    this.view = view;
    this.dateOrViewChanged();
  }

  dateOrViewChanged(): void {
    if (this.viewDate < this.minDate) {
      this.changeDate(this.minDate);
    } else if (this.viewDate >= this.maxDate) {
      this.monthLimit = true;
    } else {
      this.onDateChange.emit(this.viewDate);
    }
  }

  beforeMonthViewRender({ body }: { body: CalendarMonthViewDay[] }): void {
    let i = 0;
    body.forEach(day => {
      if (this.availableDates) {
        const date = this.findDay(day.date);
        if (date && date.cupo === 2) {
          day.cssClass = 'cal-day-free';
        }
        if (date && date.cupo === 1) {
          day.cssClass = 'cal-day-half';
        }
        if (date && date.cupo === 0) {
          day.cssClass = 'cal-day-full';
        }
      }
      if (
        this.selectedMonthViewDay &&
        day.date.getTime() === this.selectedMonthViewDay.date.getTime()
      ) {
        const find = this.findDay(day.date);
        if (find && find.cupo !== 0) {
          day.cssClass = 'cal-day-selected';
        }
        this.selectedMonthViewDay = day;
      }
      i++;
    });
  }

  beforeDayViewRender(dayView: DayViewHour[]) {
    this.dayView = dayView;
    this.addSelectedDayViewClass();
  }

  dayClicked(day: CalendarMonthViewDay): void {
    const now = new Date();
    now.setDate(now.getDate() - 1);
    if (day.date >= now) {
      if (this.selectedMonthViewDay) {
        delete this.selectedMonthViewDay.cssClass;
        if (this.availableDates) {
          const date = this.findDay(this.selectedMonthViewDay.date);
          if (date && date.cupo === 2) {
            this.selectedMonthViewDay.cssClass = 'cal-day-free';
          }
          if (date && date.cupo === 1) {
            this.selectedMonthViewDay.cssClass = 'cal-day-half';
          }
          if (date && date.cupo === 0) {
            this.selectedMonthViewDay.cssClass = 'cal-day-full';
          }
        }
      }
      const find = this.findDay(day.date);
      if (find && find.cupo !== 0) {
        day.cssClass = 'cal-day-selected';
      }
      this.selectedMonthViewDay = day;
      this.onSelectedDate.emit(day.date);
    }
  }

  private addSelectedDayViewClass() {
    this.dayView.forEach(hourSegment => {
      hourSegment.segments.forEach(segment => {
        delete segment.cssClass;
        if (
          this.selectedDayViewDate &&
          segment.date.getTime() === this.selectedDayViewDate.getTime()
        ) {
          const find = this.findDay(segment.date);
          if (find && find.cupo !== 0) {
            segment.cssClass = 'cal-day-selected';
          }
        }
      });
    });
  }

  findDay(date) {
    if (this.availableDates) {
      return this.availableDates.find(el => el.fecha
            .toISOString()
            .split(
              'T'
            )[0] === date.toISOString().split('T')[0] && el.cupo !== 0);
    }
  }
}
