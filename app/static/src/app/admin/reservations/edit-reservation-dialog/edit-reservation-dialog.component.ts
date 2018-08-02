import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Component, OnInit, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material';
import { AdminDatesService } from '../../services/admin-dates.service';
import { AdminReservationsService } from '../../services/admin-reservations.service';

@Component({
  selector: 'app-edit-reservation-dialog',
  templateUrl: './edit-reservation-dialog.component.html',
  styleUrls: ['./edit-reservation-dialog.component.scss']
})
export class EditReservationDialogComponent implements OnInit {

  error;

  datesAndTurns: FormGroup;

  pilots;

  availableDates;
  availableSchedules;
  availableTurns;
  availablePositions;

  today = new Date();
  maxReservationDate = new Date(new Date(this.today).setMonth(this.today.getMonth()+3));

  selectedPositions=[];

  positions=[
    {value: "1", PosValue:"pos1"},
    {value: "2", PosValue:"pos2"},
    {value: "3", PosValue:"pos3"},
    {value: "4", PosValue:"pos4"},
    {value: "5", PosValue:"pos5"},
    {value: "6", PosValue:"pos6"},
    {value: "7", PosValue:"pos7"},
    {value: "8", PosValue:"pos8"},
  ]
  
  myFilter = (d: Date): boolean => {
    return this.availableDates.includes(d.toISOString().substring(0,10));
  }

  constructor(
    @Inject(MAT_DIALOG_DATA) private data: any,
    private _formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<EditReservationDialogComponent>,
    private adminDatesService: AdminDatesService,
    private adminReservationService: AdminReservationsService,
  ) {
    this.datesAndTurns = this._formBuilder.group({
      date:['',Validators.required],
      schedule:['',Validators.required],
      turn_number:['',Validators.required],
      positions:[{}]
    });
   }

  ngOnInit() {
    this.pilots = this.data.pilots;
    this.getAvailableDates();

  }

  getAvailableDates(){
    let startDate = this.today.toISOString().substring(0,10);
    let endDate = new Date(new Date().setMonth(this.today.getMonth()+3)).toISOString().substring(0,10);
    this.adminDatesService.getAvailableDates(startDate,endDate).subscribe(
      res=>{
        res = res.filter(date => {
          if (date.status !== 0) {
            return date;
          }
        });        
        this.availableDates = res.map(el => el.date);
      }
    );
  }

  getAvailableSchedules(date){
    this.datesAndTurns.controls.schedule.reset();
    this.datesAndTurns.controls.turn_number.reset();
    this.availablePositions=[];
    this.selectedPositions = [];
    this.adminDatesService.getAvailableSchedules(date.toISOString().substring(0,10)).subscribe(
      res=>{
        res= res[0].schedules;
        res = res.filter(sch => {
          if (sch.status !== 0) {
            return sch;
          }
        });
        this.availableSchedules=res;
      }
    );
  }

  getAvailableTurns(schedule){
    this.datesAndTurns.controls.turn_number.reset();
    this.availablePositions=[];
    this.selectedPositions=[];
    this.availableTurns = this.availableSchedules.find(x=>x.schedule==schedule).turns;
    this.availableTurns = this.availableTurns.filter(turn=> {
      if(turn.status !== 0){
        return turn;
      }
    });
  }

  getAvailablePositions(turn){
    this.selectedPositions = [];
    this.availablePositions = this.availableTurns.find(x=>x.turn ==turn).positions;
  }

  selectPosition(position){
    if(this.selectedPositions.includes(position)){
      this.selectedPositions.splice(this.selectedPositions.indexOf(position),1);
    }else{
      this.selectedPositions.push(position);
    }
  }

  updateTurn(){
    this.error=null;
    this.error = null;
    if (this.datesAndTurns.valid && this.selectedPositions.length!==0){
      let positions = {};
      for (let i=0; i<this.selectedPositions.length; i++){
        positions['pos'+this.selectedPositions[i]]=(this.data.pilots[i])._id;
      }
      this.datesAndTurns.controls.positions.setValue(positions);

      this.adminReservationService.updateTurn(this.data._id,this.data.turns[0]._id,this.datesAndTurns.getRawValue()).subscribe(
        res=>{
          this.dialogRef.close();
        },
        err=>{
          this.error = err;
        }
      )
    }else{
      this.datesAndTurns.updateValueAndValidity();
    }
  }
}
