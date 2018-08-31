import { NewAdminDialogComponent } from './new-admin-dialog/new-admin-dialog.component';
import { DeleteAdminDialogComponent } from './delete-admindialog/delete-admindialog.component';
import { DomSanitizer } from '@angular/platform-browser';
import { EditAdminDialogComponent } from './edit-admin-dialog/edit-admin-dialog.component';
import { MatTableDataSource } from '@angular/material/table';
import { AdminService } from './../services/admin.service';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatIconRegistry } from '@angular/material/icon';

@Component({
  selector: 'app-admins',
  templateUrl: './admins.component.html',
  styleUrls: ['./admins.component.scss']
})
export class AdminsComponent implements OnInit {

  dataSource;
  displayedColumns = ['id', 'name','email','editAdmin', 'deleteAdmin']
  editAdminDialogRef;
  deleteAdminDialogRef;
  newAdminDialogRef;

  constructor(
    private adminService: AdminService,
    private dialog: MatDialog,
    private iconRegistry: MatIconRegistry,
    private sanitizer : DomSanitizer
  ) {
    this.iconRegistry
    .addSvgIcon('icn_edit', this.sanitizer.bypassSecurityTrustResourceUrl('../../assets/edit.svg'))
   }


  ngOnInit() {
    this.getAdmins();
  }

  openEditAdminDialog(element){
    this.editAdminDialogRef = this.dialog.open(EditAdminDialogComponent,{
      width: '70%',
      data: element
    });

    this.editAdminDialogRef.afterClosed().subscribe(
      ()=>{
        this.getAdmins();
      }
    )
  }

  getAdmins(){
    this.adminService.getAdmins().subscribe(
      res=>{
        this.dataSource = new MatTableDataSource(res);
      }
    )
  }

  openDeleteAdminDialog(element){
    this.deleteAdminDialogRef = this.dialog.open(DeleteAdminDialogComponent,{
      width: '70%',
      data:element
    });
    this.deleteAdminDialogRef.afterClosed().subscribe(
      ()=>{
        this.getAdmins();
      }
    )
  }

  openNewAdminDialog(){
    this.newAdminDialogRef = this.dialog.open(NewAdminDialogComponent,{
      width:'70%'
    });

    this.newAdminDialogRef.afterClosed().subscribe(
      ()=>{
        this.getAdmins();
      }
    )
  }

}
