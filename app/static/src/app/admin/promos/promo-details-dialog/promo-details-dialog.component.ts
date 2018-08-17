import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { Component, OnInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatTableDataSource } from '@angular/material';
import { EditPromoDialogComponent } from '../edit-promo-dialog/edit-promo-dialog.component';

@Component({
  selector: 'app-promo-details-dialog',
  templateUrl: './promo-details-dialog.component.html',
  styleUrls: ['./promo-details-dialog.component.scss']
})
export class PromoDetailsDialogComponent implements OnInit {

  constructor(
    @Inject(MAT_DIALOG_DATA) private data: any,
    private dialog: MatDialog,
    private dialogRef: MatDialogRef<PromoDetailsDialogComponent>,
  ) { }

  coupons;
  dataSource;
  displayedColumns: string[] = [
    'id',
    'status',
    'date_applied'
  ];

  editPromoDialogRef;
  
  promo;
  isSuperAdmin;

  ngOnInit() {  
    console.log(this.data);
    this.isSuperAdmin = this.data.isSuperAdmin;
    this.promo = this.data.promo
    this.coupons = this.data.promo.coupons;
    this.dataSource = new MatTableDataSource(this.coupons);
  }

  openEditPromoDialog(element) {
		this.editPromoDialogRef = this.dialog.open(EditPromoDialogComponent, {
      width: '70%',
      data: element
    });
    this.editPromoDialogRef.afterClosed().subscribe(
      res=>{
        this.editPromoDialogRef = null;
        this.data=res;
      }
    )
  }

  quit(){
    if(this.editPromoDialogRef){
      this.editPromoDialogRef.close();
    }
    this.dialogRef.close();
  }
}
