import { MatTableDataSource, MatSort, MatIconRegistry } from '@angular/material';
import { AdminService } from './../services/admin.service';
import { Component, OnInit, ViewChild } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

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

  @ViewChild(MatSort) sort: MatSort;

  constructor(
    private adminService: AdminService,
    private iconRegistry   : MatIconRegistry,
    private sanitizer      : DomSanitizer
  ) {
    this.iconRegistry
    .addSvgIcon('icn_authorize', this.sanitizer.bypassSecurityTrustResourceUrl('../../assets/checked.svg'))
    .addSvgIcon('icn_cancel', this.sanitizer.bypassSecurityTrustResourceUrl('../../assets/cancel.svg'))
   }

  ngOnInit() {
    this.getUnprintedLicenses();
  }

  getUnprintedLicenses(){
    this.adminService.getUnprintedLicenses().subscribe(
      res=>{
        this.dataSourceLicenses = new MatTableDataSource(res);
        this.dataSourceLicenses.sort = this.sort;
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
    this.adminService.changePrintStatus(id).subscribe(
      res=>{
        this.getUnprintedLicenses();
      },
      err=>{
        this.error = err;
        this.closeBanner();
      }
    )
  }

  changePrinted(id){
    this.adminService.changePrintStatus(id).subscribe(
      res=>{
        this.getUnprintedLicenses();
      }
    )
  }

  closeBanner(){
    setTimeout(()=>{
      this.error = null;
    }, 12000);
  }
}
