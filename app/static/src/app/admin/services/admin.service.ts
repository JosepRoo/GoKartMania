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
export class AdminService {
  private apiAdmin: string = environment.api + '/admin';
  private apiLogout: string = environment.api + '/logout';
  private headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Accept: 'application/json'
  });

  constructor(
    private http: HttpClient,
    private router: Router,
    private location: Location
  ) {}

  getBusyHours(): Observable<any[]> {
    return this.http
      .get<any>(this.apiAdmin + '/busy_hours', { headers: this.headers })
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

  getAveragePrice(): Observable<any> {
    return this.http
      .get<any>(this.apiAdmin + '/reservation_avg_price', {
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

  getIncome(start, end): Observable<any> {
    return this.http
      .get<any>(
        this.apiAdmin + '/reservation_income_qty/' + start + '/' + end,
        {
          headers: this.headers
        }
      )
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

  getPromosIncome(start, end): Observable<any> {
    return this.http
      .get<any>(
      this.apiAdmin + '/promos_income_qty/' + start + '/' + end,
        {
          headers: this.headers
        }
      )
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

  getUnprintedLicenses(){
    return this.http
      .get<any>(
        this.apiAdmin + '/unprinted_licenses/Carso',
      {
        headers: this.headers
      }
      )
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

  blockTurns(body){
    return this.http
      .post<any>(
        this.apiAdmin + '/block_turns/True',
        body,
        {
          headers: this.headers
        }
      )
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

  unblockTurns(body){
    return this.http
      .post<any>(
        this.apiAdmin + '/block_turns/False',
        body,
        {
          headers: this.headers
        }
      )
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


  // CHECK
  loginAdmin(body) {
    body.name = 'name';
    return this.http
    .post<any>(
      this.apiAdmin,
      body,
      {
        headers: this.headers
      }
    )
    .pipe( res => {
      
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

  logOutAdmin():Observable<any>{
    return this.http.post<any>(this.apiLogout,{headers:this.headers})
    .pipe(res=>{
      this.location.replaceState('/');
      this.router.navigate(['logIn']);
      return res;
    })
    .catch(e=>{
      return Observable.throw(e.error.message);
    });
  }

  changePrintStatus(id){
    return this.http.put<any>(this.apiAdmin+"/unprinted_licenses/Carso/"+id,null,{headers:this.headers})
    .pipe( res => {
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

  getAdmins(){
    return this.http.get<any>(this.apiAdmin+"/admins",{headers:this.headers})
    .pipe( res => {
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

  editAdmin(body){
    return this.http.put<any>(this.apiAdmin+"/alter_admin",body,{headers:this.headers})
    .pipe( res => {
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

  deleteAdmin(id){
    return this.http.delete<any>(this.apiAdmin+"/alter_admin/"+id,{headers:this.headers})
    .pipe( res => {
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

  createAdmin(body){
    return this.http.post<any>(this.apiAdmin+"/alter_admin",body,{headers:this.headers})
    .pipe( res => {
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

  getBlockedTurns(date){
    return this.http.get<any>(this.apiAdmin+"/blocked_turns/"+date,{headers:this.headers})
    .pipe( res => {
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
