import { AdminReservationsService } from './../../services/admin-reservations.service';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-create-report-dialog',
  templateUrl: './create-report-dialog.component.html',
  styleUrls: ['./create-report-dialog.component.scss']
})
export class CreateReportDialogComponent implements OnInit {

  reservationsReport: FormGroup;

  error;

  minDate = new Date("1920/1/1");
  endDateMin;

  constructor(
    private _formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<CreateReportDialogComponent>,
    private adminReservationsService: AdminReservationsService
  ) {
    this.reservationsReport = this._formBuilder.group({
      startDate:['',Validators.required],
      endDate:['',Validators.required]
    });
   }

  ngOnInit() {

  }

  createReport(){
    this.error = null;
    if (this.reservationsReport.valid){
      let startDate = this.reservationsReport.controls.startDate.value.toISOString().substring(0,10);
      let endDate = this.reservationsReport.controls.endDate.value.toISOString().substring(0,10);
      this.adminReservationsService.generateReport(startDate, endDate);
      this.dialogRef.close();
    }else{
      this.error = "Por favor llena todos los campos"
      this.reservationsReport.get('startDate').updateValueAndValidity();
      this.reservationsReport.get('endDate').updateValueAndValidity();
      this.reservationsReport.updateValueAndValidity(); 
    }
  }

  changeMinDate(date){
		let startDate = new Date(date);
		let startDay = startDate.getDate();
		this.endDateMin = new Date(new Date(startDate).setDate(startDay+1));
  }
}
