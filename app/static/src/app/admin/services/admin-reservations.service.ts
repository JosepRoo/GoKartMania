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
export class AdminReservationsService {
  private apiReservations: string = environment.api + '/admin/licensed_pilots';
  private apiUpcomingReservations = environment.api + '/user/reservations';
  private headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Accept: 'application/json'
  });

  constructor(
    private http: HttpClient,
    private router: Router,
    private location: Location
  ) {}

  getReservations(): Observable<any[]> {
    return this.http
      .get<any>(this.apiReservations, {
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

  getUpcomingReservations(date){
    return this.http
    .get<any>(this.apiUpcomingReservations+'/'+date+'/'+date.substring(0,4)+'-12-31',{
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
