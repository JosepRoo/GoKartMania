import { AdminService } from './../../services/admin.service';
import { Component, OnInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-edit-admin-dialog',
  templateUrl: './edit-admin-dialog.component.html',
  styleUrls: ['./edit-admin-dialog.component.scss']
})
export class EditAdminDialogComponent implements OnInit {

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private _formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<EditAdminDialogComponent>,
    private adminService: AdminService
  ) {
    this.adminData = this._formBuilder.group({
      _id:[this.data._id],
			name: [this.data.name, [Validators.required]],
      email: [this.data.email, [Validators.required]],
      changePassword: [],
      password:  [this.data.password]
    });
   }

  adminData: FormGroup;

  error;


  ngOnInit() {
  }

  changePassword(){
    if(this.adminData.controls.changePassword.value){
      this.adminData.controls.password.setValidators(Validators.required);
      this.adminData.controls.password.setValue(null);
		}else{
      this.adminData.controls.password.setValidators(null);
      this.adminData.controls.password.setValue(this.data.password);
		}
  }

  editAdmin(){
    this.adminService.editAdmin(this.adminData.getRawValue()).subscribe(
      res=>{
        this.dialogRef.close();
      },
      err=>{
        this.error = err;
      }
    )
  }
}