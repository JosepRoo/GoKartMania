import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

@Injectable({
  providedIn: 'root'
})
export class AdminDatesService {
  // private apiAvailableDates = environment.api + '/admin/available_dates';
  private apiAvailableDates = environment.api + '/admin/available_dates';
  private apiAvailableSchedules = environment.api + '/admin/available_schedules';

  private headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Accept: 'application/json'
  });

  constructor(
    private http: HttpClient,
    private router: Router,
    private location: Location
  ) {}

  getAvailableDates(startDate, endDate) {
    return this.http
    .get<any>(this.apiAvailableDates + '/' + startDate + '/' + endDate, {
      headers: this.headers
    })
    .pipe(res => {
      return res;
    })
    .catch(e => {
      if (e.status === 401) {
        this.location.replaceState('/');
        this.router.navigate(['/logIn']);
        return Observable.throw(e.error.message);
      }
      if (e.status === 400) {
        return Observable.throw(e.error.message);
      }
    });
  }

  getAvailableSchedules(date: string) {
    return this.http
    .get<any>(this.apiAvailableSchedules + '/' + date, {
      headers: this.headers
    })
    .pipe(res => {
      return res;
    })
    .catch(e => {
      if (e.status === 401) {
        this.location.replaceState('/');
        this.router.navigate(['/logIn']);
        return Observable.throw(e.error.message);
      }
      if (e.status === 400) {
        return Observable.throw(e.error.message);
      }
    });
  }
}
