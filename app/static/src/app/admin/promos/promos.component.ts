import { MatDialog } from '@angular/material/dialog';
import { Component, OnInit, ViewChild} from '@angular/core';
import { MatSort, MatTableDataSource, MatIconRegistry } from '@angular/material';
import { DomSanitizer } from '@angular/platform-browser';

//components
import { NewPromoDialogComponent } from './new-promo-dialog/new-promo-dialog.component';
import { EditPromoDialogComponent } from './edit-promo-dialog/edit-promo-dialog.component';

//services
import { PromosService } from './../services/promos.service';

@Component({
  selector: 'app-promos',
  templateUrl: './promos.component.html',
  styleUrls: ['./promos.component.scss']
})
export class PromosComponent implements OnInit {
  promos = [];
  dataSource;
  defaultDate = new Date().getTime();

  displayedColumns: string[] = [
    'authorised',
    'type',
    'value',
    'existence',
    'start_date',
    'end_date',
    'actions',
    
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


	openNewPromoDialog() {
		const newPromoDialogRef = this.dialog.open(NewPromoDialogComponent, {
			width: '70%'
		});

		newPromoDialogRef.afterClosed().subscribe(
			()=>{
        this.getPromos();
			}
		);
  }

  getPromos(){
    this.promosService.getPromos().subscribe(res => {
      this.promos = [];
      if (res.isSuperAdmin && (this.displayedColumns[this.displayedColumns.length-1])=='actions'){
        // this.displayedColumns.push('downloads');
        this.displayedColumns.push('authorize');
      }
      let promos = res.promos;
      
      for (let element of promos){
        if(Date.parse(element.end_date) > this.defaultDate){
          this.promos.push(element);
        }
      }
      this.dataSource = new MatTableDataSource(this.promos);
      this.dataSource.sort = this.sort;
    });
  }
  

  authorizePromo(element,authorized){
    element.authorised = authorized;
    element.password = null;
    this.promosService.changePromo(element).subscribe(
      res=>{
        this.getPromos();
      },
      err=>{
        console.log("err");
      }
    )
  }

  openEditPromoDialog(element) {
		const editPromoDialogRef = this.dialog.open(EditPromoDialogComponent, {
      width: '70%',
      data: element
    });
    editPromoDialogRef.afterClosed().subscribe(
      ()=>{
        this.getPromos();
      }
    )
  }

  // exportCoupons(coupons){

  // }
}
