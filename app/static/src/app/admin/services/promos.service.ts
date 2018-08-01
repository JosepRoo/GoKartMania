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
export class PromosService {
  private apiPromos: string = environment.api + '/promos';
  private headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Accept: 'application/json'
  });

  constructor(
    private http: HttpClient,
    private router: Router,
    private location: Location
  ) { }

  getPromos(): Observable<{promos: any, isSuperAdmin: any}> {
    return this.http
      .get<any>(this.apiPromos, {
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

  createPromo(body): Observable<any>{
    return this.http.post(this.apiPromos,body,{headers:this.headers})
    .pipe(res=>{
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


  //  CHECK
  changePromo(body): Observable<any>{
    return this.http.put(this.apiPromos+'/'+body._id,body, {headers:this.headers})
    .pipe(res=>{
      return res
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
