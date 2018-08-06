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
  private apiReservations = environment.api + '/user/reservations';
  private apiTurns = environment.api + '/user/turns';
  private apiTurn = environment.api + '/user/turn';
  private apiPayment = environment.api + '/user/payments';
  private apiUser = environment.api + '/user';
  private headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Accept: 'application/json'
  });

  constructor(
    private http: HttpClient,
    private router: Router,
    private location: Location
  ) {}

  getUpcomingReservations(date):Observable<any>{
    return this.http
    .get<any>(this.apiReservations+'/'+date+'/'+date.substring(0,4)+'-12-31',{
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

  addReservation(reservation): Observable<any[]> {
    return this.http
      .post<any>(this.apiReservations, reservation, {
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

  addTurn(turn): Observable<any>{
    turn.date = turn.date.toISOString().substring(0,10);
    return this.http
    .post<any>(this.apiTurns,turn,{
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
      if (e.status === 400 || e.status ===409) {
        return Observable.throw(e.error.message);
      }
    });
  }

  getReservations():Observable<any>{
    return this.http
    .get<any>(this.apiReservations,{
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

  payReservationAsAdmin(userID){    
    let body = {
      "coupon_id": null,
      "cvv": null,
      "month": null,
      "name": null,
      "number": null,
      "payment_method": null,
      "payment_type": "Admin",
      "promo_id": null,
      "user_email": null,
      "user_id": null,
      "user_name": null,
      "year": null
    }

    return this.http
    .post<any>(this.apiPayment+'/'+userID,body,{
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

  setUserToPay(body){
    return this.http
    .post<any>(this.apiUser,body,{
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

  updateTurns(reservationId:string, body){
    return this.http
    .put<any>(this.apiTurn+'/'+reservationId,body,{
      headers:this.headers
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
      if (e.status === 400 || e.status ===409) {
        return Observable.throw(e.error.message);
      }
    }); 
  }

  generateReport(startDate: string, endDate:string){
    let url = environment.api + '/admin/build_reservations_report/' + startDate+'/'+endDate;

    window.open(url);
  }
}
