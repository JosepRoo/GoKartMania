
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { environment } from '../../../environments/environment';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

@Injectable({
  providedIn: 'root'
})
export class AdminPilotsService {
  private apiPilots: string = environment.api + '/admin/licensed_pilots';
  private apiRegisterPilots: string = environment.api + '/user/pilots';
  private headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Accept: 'application/json'
  });

  constructor(
    private http: HttpClient,
    private router: Router,
    private location: Location
  ) {}

  getPilots(): Observable<any[]> {
    return this.http
      .get<any>(this.apiPilots, {
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

  registerPilots(pilots): Observable<any[]> {
    const data = {
      pilots : pilots
    };
    return this.http
      .post<any>(this.apiRegisterPilots, data, { headers: this.headers })
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

  generateReport(){
    let url = environment.api+ '/admin/build_pilots_report';

    window.open(url);
  }
}
