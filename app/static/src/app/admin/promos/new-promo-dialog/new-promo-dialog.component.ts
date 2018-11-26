import { PromosService } from './../../services/promos.service';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Component, OnInit, ViewChild } from '@angular/core';

@Component({
	selector: 'app-new-promo-dialog',
	templateUrl: './new-promo-dialog.component.html',
	styleUrls: ['./new-promo-dialog.component.scss']
})
export class NewPromoDialogComponent implements OnInit {

	promoData: FormGroup;
	defaultDate = new Date();
	endDateMin;
	
	placeholderValue = "";
	placeholderRequiredRaces = "Número exacto de carreras necesarias";

	error;
	

	constructor(
	private _formBuilder: FormBuilder,
	private dialogRef: MatDialogRef<NewPromoDialogComponent>,
	private promosService: PromosService
	) {
		this.promoData = this._formBuilder.group({
			start_date: ['', [Validators.required]],
			end_date: ['', [Validators.required]],
			type: ['', [Validators.required]],
			existence: ['', [Validators.required]],
			copies_left:['', Validators.required],
			description: ['', [Validators.required]],
			value: ['',[Validators.required]],
			password: ['',[Validators.required]],
			setPrefix:[],
			prefix:[],
			at_least:[],
			required_races:[Validators.required]
		});
	}

	ngOnInit() {
		
	}

	changeSetPrefix(){
		if(this.promoData.controls.setPrefix.value){
			this.promoData.controls.prefix.setValidators(Validators.required);
		}else{
			this.promoData.controls.prefix.setValidators(null);
		}
	}

	changeAtLeast(){
		if (this.promoData.controls.at_least.value){
			this.placeholderRequiredRaces = "Número mínimo de carreras necesarias";
		}else{
			this.placeholderRequiredRaces = "Número exacto de carreras necesarias";
		}
	}

	createPromo(){
		this.error= null;
		if (this.promoData.valid){
			let data = this.promoData.getRawValue();
			data.start_date = new Date(data.start_date).toISOString().substring(0,10);
			data.end_date = new Date(data.end_date).toISOString().substring(0,10);
			this.promosService.createPromo(data).subscribe(
				res=>{
					this.dialogRef.close();
				},
				err=>{
				  this.error = err;
				}
			);
		}else{
			this.promoData.updateValueAndValidity();
		}
	}

	changeMinDate(){
		let startDate = new Date(this.promoData.controls.start_date.value);
		let startDay = startDate.getDate();
		this.endDateMin = new Date(new Date(startDate).setDate(startDay+1));
	}

	changePlaceholder(){
		if (this.promoData.controls.type.value == "Descuento"){
			this.placeholderValue = "% de descuento";
			this.promoData.controls.value.setValidators(Validators.required);
		} else if (this.promoData.controls.type.value == "Reservación") {
			this.promoData.controls.value.setValue(1);
		 }
		else{
			this.placeholderValue = "No. de carreras";
			this.promoData.controls.value.setValidators(Validators.required);
		}
	}
}
