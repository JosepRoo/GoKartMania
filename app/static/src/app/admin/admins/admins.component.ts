import { NewAdminDialogComponent } from './new-admin-dialog/new-admin-dialog.component';
import { DeleteAdminDialogComponent } from './delete-admindialog/delete-admindialog.component';
import { DomSanitizer } from '@angular/platform-browser';
import { EditAdminDialogComponent } from './edit-admin-dialog/edit-admin-dialog.component';
import { MatTableDataSource } from '@angular/material/table';
import { AdminService } from './../services/admin.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatIconRegistry } from '@angular/material/icon';

@Component({
  selector: 'app-admins',
  templateUrl: './admins.component.html',
  styleUrls: ['./admins.component.scss']
})
export class AdminsComponent implements OnInit, OnDestroy {

  dataSource;
  displayedColumns = ['id', 'name','email','editAdmin', 'deleteAdmin']
  editAdminDialogRef;
  deleteAdminDialogRef;
  newAdminDialogRef;s

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
  
  ngOnDestroy(){
    if (this.editAdminDialogRef){
      this.editAdminDialogRef.close();
    }
    if(this.deleteAdminDialogRef){
      this.deleteAdminDialogRef.close();
    }
    if(this.newAdminDialogRef){
      this.newAdminDialogRef.close();
    }
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
