import { AdminService } from './../admin/services/admin.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.scss']
})
export class LogInComponent implements OnInit {
  logIn: FormGroup;
  loginError:string;
  constructor(
    private formBuilder: FormBuilder,
    private adminService: AdminService,
    private router: Router,
    private location: Location
  ) { }

  ngOnInit() {
    this.logIn = this.formBuilder.group({
      email: ['',[Validators.required, Validators.email]],
      password:['',[Validators.required]]
    });
  }

  loginAdmin(){
    if(this.logIn.valid){
      this.adminService.loginAdmin(this.logIn.getRawValue()).subscribe(
        res=>{
          this.location.replaceState('/');
          this.router.navigate(['admin/home']);
        },
        err =>{
          this.loginError = err;
        }
      );
    }else{
      this.logIn.updateValueAndValidity();
    }
  }
}
