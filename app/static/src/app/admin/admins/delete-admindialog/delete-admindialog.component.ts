import { AdminService } from './../../services/admin.service';
import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-delete-admindialog',
  templateUrl: './delete-admindialog.component.html',
  styleUrls: ['./delete-admindialog.component.scss']
})
export class DeleteAdminDialogComponent implements OnInit {

  constructor(
    private dialogRef: MatDialogRef<DeleteAdminDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private adminService: AdminService
  ) { }

  ngOnInit() {
  }

  deleteAdmin(){
    this.adminService.deleteAdmin(this.data._id).subscribe(
      res=>{
        this.dialogRef.close()
      },
      err=>{
        this.dialogRef.close(err);
      }
    )
  }
}
