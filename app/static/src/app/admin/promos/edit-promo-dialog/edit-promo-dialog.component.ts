import { PromosService } from './../../services/promos.service';
import { Component, OnInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-edit-promo-dialog',
  templateUrl: './edit-promo-dialog.component.html',
  styleUrls: ['./edit-promo-dialog.component.scss']
})
export class EditPromoDialogComponent implements OnInit {

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private _formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<EditPromoDialogComponent>,
    private promosService: PromosService
) { }

  defaultDate = new Date();
  startDate = Date.parse(this.data.start_date);
  endDate = Date.parse(this.data.end_date);
  endDateMin;

  promoData: FormGroup;

  error;

  ngOnInit() {
    this.promoData = this._formBuilder.group({
			start_date: [this.data.start_date, [Validators.required]],
			end_date: [this.data.end_date, [Validators.required]],
    });
    this.changeMinDate(this.defaultDate);
  }

  changeMinDate(date){
		let startDate = new Date(date);
		let startDay = startDate.getDate();
		this.endDateMin = new Date(new Date(startDate).setDate(startDay+1));
  }
  
  editPromo(){
    this.error = null;
    if(this.promoData.valid){
      this.data.start_date = new Date(this.promoData.controls.start_date.value).toISOString().substring(0,10);
      this.data.end_date =  new Date(this.promoData.controls.end_date.value).toISOString().substring(0,10);
      this.data.password = null;
      this.promosService.changePromo(this.data).subscribe(
        res=>{
          this.dialogRef.close(res);
        },
        err=>{
          this.error = err;
        }
      );
    }
  }

}
