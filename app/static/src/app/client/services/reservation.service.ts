import { PilotService } from './pilot.service';
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
export class ReservationService {
  private reservationApi: string = environment.api + '/user/reservations';
  private promosApi: string = environment.api + '/user/reservations_promo';
  private userApi: string = environment.api + '/user';
  private paymentsApi: string = environment.api + '/user/payments';
  private turnsApi: string = environment.api + '/user/alter_turn';
  private headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Accept: 'application/json'
  });

  constructor(
    private http: HttpClient,
    private router: Router,
    private location: Location
  ) {}

  addReservation(reservation): Observable<any[]> {
    return this.http
      .post<any>(this.reservationApi, reservation, {
        headers: this.headers
      })
      .pipe(res => {
        return res;
      })
      .catch(e => {
        if (e.status === 401) {
          this.location.replaceState('/');
          this.router.navigate(['/instrucciones']);
          return Observable.throw(e.error.message);
        }
        if (e.status === 400) {
          return Observable.throw(e.error.message);
        }
      });
  }

  getReservation(): Observable<any> {
    return this.http
      .get<any>(this.reservationApi, {
        headers: this.headers
      })
      .pipe(res => {
        return res;
      })
      .catch(e => {
        if (e.status === 401) {
          this.location.replaceState('/');
          this.router.navigate(['/instrucciones']);
          return Observable.throw(e.error.message);
        }
        if (e.status === 400) {
          return Observable.throw(e.error.message);
        }
      });
  }

  putPromo(promo): Observable<any> {
    return this.http
      .put<any>(this.promosApi, promo, { headers: this.headers })
      .pipe(res => {
        return res;
      })
      .catch(e => {
        if (e.status === 401) {
          return Observable.throw(e.error.message);
        }
        if (e.status === 400) {
          return Observable.throw(e.error.message);
        }
      });
  }

  postUser(user): Observable<any> {
    return this.http
      .post<any>(this.userApi, user, { headers: this.headers })
      .pipe(res => {
        return res;
      })
      .catch(e => {
        if (e.status === 401) {
          return Observable.throw(e.error.message);
        }
        if (e.status === 400) {
          return Observable.throw(e.error.message);
        }
      });
  }

  postPayment(payment): Observable<any> {
    return this.http
      .post<any>(this.paymentsApi + '/' + payment.user_id, payment, {
        headers: this.headers
      })
      .pipe(res => {
        return res;
      })
      .catch(e => {
        if (e.status === 401) {
          return Observable.throw(e.error.message);
        }
        if (e.status === 400) {
          return Observable.throw(e.error.message);
        }
      });
  }

  deleteTurn(id,date){
    return this.http
      .delete<any>(this.turnsApi + '/' + id +'/'+date,{
        headers: this.headers,
      })
      .pipe(res => {
        return res;
      })
      .catch(e => {
        if (e.status === 401) {
          return Observable.throw(e.error.message);
        }
        if (e.status === 400) {
          return Observable.throw(e.error.message);
        }
      });
  }
}
