import { MatDialog } from '@angular/material/dialog';
import { Component, OnInit, ViewChild, OnDestroy} from '@angular/core';
import { MatSort, MatTableDataSource, MatIconRegistry } from '@angular/material';
import { DomSanitizer } from '@angular/platform-browser';
import * as XLSX from 'xlsx';

//components
import { NewPromoDialogComponent } from './new-promo-dialog/new-promo-dialog.component';
import { EditPromoDialogComponent } from './edit-promo-dialog/edit-promo-dialog.component';

//services
import { PromosService } from './../services/promos.service';
import { PromoDetailsDialogComponent } from './promo-details-dialog/promo-details-dialog.component';

@Component({
  selector: 'app-promos',
  templateUrl: './promos.component.html',
  styleUrls: ['./promos.component.scss']
})
export class PromosComponent implements OnInit, OnDestroy {
  promos = [];
  dataSource;
  editPromoDialogRef;
  newPromoDialogRef;
  promoDetailsDialogRef;
  defaultDate = new Date().getTime();
  isSuperAdmin;

  displayedColumns: string[] = [
    'authorised',
    'type',
    'value',
    'existence',
    'start_date',
    'end_date'
  ];
  @ViewChild(MatSort) sort: MatSort;

  constructor(
    private promosService: PromosService,
    private dialog: MatDialog,
    private iconRegistry   : MatIconRegistry,
    private sanitizer      : DomSanitizer
  ) {
    this.iconRegistry
    .addSvgIcon('icn_authorize', this.sanitizer.bypassSecurityTrustResourceUrl('../../assets/checked.svg'))
    .addSvgIcon('icn_cancel', this.sanitizer.bypassSecurityTrustResourceUrl('../../assets/cancel.svg'))
    .addSvgIcon('icn_edit', this.sanitizer.bypassSecurityTrustResourceUrl('../../assets/edit.svg'))
  }


  ngOnInit() {
    this.getPromos();
  }

  ngOnDestroy(){
    if (this.newPromoDialogRef){
      this.newPromoDialogRef.close();
    }
    if(this.editPromoDialogRef){
      this.editPromoDialogRef.close();
    }
    if (this.promoDetailsDialogRef){
      this.promoDetailsDialogRef.quit();
    }
  }


	openNewPromoDialog() {
		this.newPromoDialogRef = this.dialog.open(NewPromoDialogComponent, {
			width: '70%'
		});

		this.newPromoDialogRef.afterClosed().subscribe(
			()=>{
        this.getPromos();
        this.newPromoDialogRef = null;
			}
		);
  }

  getPromos(){
    this.promosService.getPromos().subscribe(res => {
      this.promos = [];
      this.isSuperAdmin=res.isSuperAdmin;
      if (this.isSuperAdmin && (this.displayedColumns[this.displayedColumns.length-1])=='end_date'){
        this.displayedColumns.push('actions');
        this.displayedColumns.push('authorize');
        this.displayedColumns.push('download');
      }
      let promos = res.promos;
      
      for (let element of promos){
        if(Date.parse(element.end_date) > this.defaultDate){
          this.promos.push(element);
        }
      }
      this.dataSource = new MatTableDataSource(this.promos);
      this.dataSource.sort = this.sort;
      console.log(this.dataSource);
    });
  }
  

  authorizePromo(element,authorized){
    element.authorised = authorized;
    element.password = null;
    this.promosService.changePromo(element).subscribe(
      res=>{
        this.getPromos();
      }
    )
  }

  openEditPromoDialog(element) {
		this.editPromoDialogRef = this.dialog.open(EditPromoDialogComponent, {
      width: '30%',
      data: element
    });
    this.editPromoDialogRef.afterClosed().subscribe(
      ()=>{
        this.getPromos();
        this.editPromoDialogRef = null;
      }
    )
  }

  exportCoupons(coupons){
    let excelFileName = "Cupones";
    const workbook: XLSX.WorkBook = XLSX.utils.book_new();
    const worksheet: XLSX.WorkSheet = XLSX.utils.json_to_sheet(coupons);
    
    XLSX.utils.book_append_sheet(workbook, worksheet, 'data');
    XLSX.writeFile(workbook, 'Cupones.xlsx');

  }

  openPromoDetail(promo, isSuperAdmin){
    this.promoDetailsDialogRef = this.dialog.open(PromoDetailsDialogComponent,{
      width: '50%',
      data:{
        'promo': promo,
        'isSuperAdmin': isSuperAdmin
      },
      maxHeight: 600
    });
    this.promoDetailsDialogRef.afterClosed().subscribe(
      ()=>{
        this.getPromos();
        this.editPromoDialogRef=null;
        this.promoDetailsDialogRef=null;
      }
    );
  }
}
