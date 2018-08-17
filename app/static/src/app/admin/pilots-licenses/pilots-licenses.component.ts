import { MatTableDataSource } from '@angular/material';
import { AdminService } from './../services/admin.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-pilots-licenses',
  templateUrl: './pilots-licenses.component.html',
  styleUrls: ['./pilots-licenses.component.scss']
})
export class PilotsLicensesComponent implements OnInit {

  dataSourceLicenses;
  error;
  displayedColumnsLicenses: string[] = [
    'id',
    'name',
    'last_name',
    'printed',
    'print_license'
  ];

  constructor(
    private adminService: AdminService
  ) { }

  ngOnInit() {
    this.getUnprintedLicenses();
  }

  getUnprintedLicenses(){
    this.adminService.getUnprintedLicenses().subscribe(
      res=>{
        this.dataSourceLicenses = new MatTableDataSource(res);
      },
      err=>{
        this.error = err;
        this.closeBanner();
      }
    )
  }

  printLicense(element){
    this.error = null;
    let location = element.location;
    let id = element._id;
    element.licensed = true;
    this.adminService.setLicenseAsPrinted(location,id,element).subscribe(
      res=>{
        this.getUnprintedLicenses();
      },
      err=>{
        this.error = err;
        this.closeBanner();
      }
    )
  }

  closeBanner(){
    setTimeout(()=>{
      this.error = null;
    }, 12000);
  }
}
