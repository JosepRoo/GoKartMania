import { AdminService } from './../../services/admin.service';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { PasswordValidation } from './password-validation';

@Component({
  selector: 'app-new-admin-dialog',
  templateUrl: './new-admin-dialog.component.html',
  styleUrls: ['./new-admin-dialog.component.scss']
})
export class NewAdminDialogComponent implements OnInit {

  adminData: FormGroup;
  error;
  
  constructor(
    private _formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<NewAdminDialogComponent>,
    private adminService: AdminService
  ) {
    
    this.adminData = this._formBuilder.group({
			name: ['', [Validators.required]],
      email: ['', [Validators.required]],
      password: ['', Validators.required],
      confirmPassword: ['']
    },{
      validator: PasswordValidation.MatchPassword 
    });
   }

  ngOnInit() {
  }

  createAdmin(){
    this.adminService.createAdmin(this.adminData.getRawValue()).subscribe(
      res=>{
        this.dialogRef.close();
      },
      err=>{
        this.error = err;
      }
    )
  }
}