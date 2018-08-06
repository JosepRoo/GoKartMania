import { AdminReservationsService } from './../../services/admin-reservations.service';
import { FormBuilder, FormGroup, Validators, FormControl, FormArray } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { AdminDatesService } from './../../services/admin-dates.service';
import { Component, OnInit, Inject } from "@angular/core";


@Component({
  selector: 'app-edit-reservation-dialog',
  templateUrl: './edit-reservation-dialog.component.html',
  styleUrls: ['./edit-reservation-dialog.component.scss']
})


export class EditReservationDialogComponent implements OnInit {

  error;

  today = new Date();
  maxReservationDate = new Date(new Date(this.today).setMonth(this.today.getMonth()+3));

  datesAndTurns: FormGroup;

  reservationTurns;
  pilots;
  positions = [
    {value: "pos1", viewValue: 1, selected: false},
    {value: "pos2", viewValue: 2, selected: false},
    {value: "pos3", viewValue: 3, selected: false},
    {value: "pos4", viewValue: 4, selected: false},
    {value: "pos5", viewValue: 5, selected: false},
    {value: "pos6", viewValue: 6, selected: false},
    {value: "pos7", viewValue: 7, selected: false},
    {value: "pos8", viewValue: 8, selected: false}
  ];

  result;
  display;

  availableDates;
  availableSchedules = [];
  availableTurns = [];
  availablePositions = [];

  selectedPositions = [];

  myFilter = (d: Date): boolean => {
    return this.availableDates.includes(d.toISOString().substring(0,10));
  }

  constructor(
    private adminDatesService: AdminDatesService,
    private dialogRef: MatDialogRef<EditReservationDialogComponent>,
    private _formBuilder: FormBuilder,
    private adminReservationsService: AdminReservationsService,
    @Inject(MAT_DIALOG_DATA) private data: any,
  ){
    this.datesAndTurns = this._formBuilder.group({
      date: [this.data.date,Validators.required],
      turns: this._formBuilder.array([])
    })
  }

  ngOnInit(){
    console.log("DATA",this.data);
    this.display=false;
    this.getAvailableDates();
    this.getAvailableSchedules(this.data.date.substring(0,10));

    this.reservationTurns = this.data.turns;
    this.pilots= this.data.pilots;
    const formTurns = this.datesAndTurns.get('turns') as FormArray;
    for (let turn of this.reservationTurns){
      this.availableTurns.push([]);
      this.availablePositions.push([]);
      this.selectedPositions.push([]);
    }

    for(let i = 0; i < this.reservationTurns.length; i++){
      this.getAvailableTurns(this.data.turns[i].schedule,i);
      this.getAvailablePositions(this.data.turns[i].schedule,this.data.turns[i].turn_number,i)
      this.selectedPositions[i] = Object.keys(this.reservationTurns[i].positions);
      formTurns.push(this.createReservationTurns(this.reservationTurns[i].schedule, this.reservationTurns[i].turn_number,i));
    }
  }

  createReservationTurns(schedule, turn_number, i){
    return this._formBuilder.group({
      schedule: [schedule, Validators.required],
      turn_number: [+turn_number, Validators.required],
      positions: this.createReservationTurnsPositions(i)
    })
  }

  createReservationTurnsPositions(i){
    const arr = this.positions.map(position=>{
      if (this.selectedPositions[i].includes(position.value)){
        return new FormControl(true);
      }else{
        return new FormControl(false);
      }
    }); 
    return this._formBuilder.array(arr);
  }

  getAvailableDates(){
    let startDate = this.today.toISOString().substring(0,10);
    let endDate = this.maxReservationDate.toISOString().substring(0,10);
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

  getDatesAndTurnsData(){
    return this.datesAndTurns.get('turns') as FormArray;
  }

  getTurnsData(i){
    return this.getDatesAndTurnsData().controls[i].get('positions');
  }

  getAvailableSchedules(date){
    this.result= null;
    this.availableSchedules = [];
    this.adminDatesService.getAvailableSchedules(date).subscribe(
      res=>{
        res= res[0].schedules;
        res = res.filter(sch => {
          if (sch.status !== 0) {
            this.availableSchedules.push(sch.schedule);
            return sch;
          }
        });
        this.result=res;
      }
    )
  }

  getAvailableTurns(schedule,i){
    this.availableTurns[i]=[];
    if (this.result){
      console.log(this.result);

      let arr =this.result.find(x=>x.schedule==schedule).turns;
      arr.filter(turn=>{
        if(turn.status !== 0){
          this.availableTurns[i].push(turn.turn);
        }
      });
    }else{
      setTimeout(()=>{
        this.getAvailableTurns(schedule,i);
      },500);
    }
  }

  getAvailablePositions(schedule, turn,i){
    if (this.result){
      let arr =this.result.find(x=>x.schedule==schedule).turns;
      arr = arr.find(x=>x.turn ==turn).positions;
      this.availablePositions[i]= arr;
      console.log("AP",this.availablePositions);
      if(this.availablePositions[this.availablePositions.length-1].length!==0){
        this.display=true;
      }
    }else{
      setTimeout(()=>{
        this.getAvailablePositions(schedule,turn,i);
      },500);
    }
  }

  changeDate(){
    let turns = this.datesAndTurns.get('turns').value;
    console.log("FECHA",this.datesAndTurns.controls.date.value.toISOString().substring(0,10));
    this.getAvailableSchedules(this.datesAndTurns.controls.date.value.toISOString().substring(0,10));
    for(let i = 0; i <  this.reservationTurns.length;i++){
      console.log("SCH",turns[i].schedule);
      this.getAvailableTurns(turns[i].schedule,i);
      this.getAvailablePositions(turns[i].schedule,turns[i].turn_number,i);
    }
  }

  changeSchedule(){
    let turns = this.datesAndTurns.get('turns').value;
    for (let i = 0; i<this.reservationTurns.length;i++){
      this.getAvailableTurns(turns[i].schedule,i);
      this.getAvailablePositions(turns[i].schedule,turns[i].turn_number,i);
    }
  }

  changeTurn(){
    let turns = this.datesAndTurns.get('turns').value;
    for (let i = 0; i<this.reservationTurns.length;i++){
      this.getAvailablePositions(turns[i].schedule,turns[i].turn_number,i);
    }
  }

  changePositions(i,j){
    if(this.selectedPositions[i].includes(this.positions[j].value)){
      this.selectedPositions[i].splice(this.selectedPositions[i].indexOf(this.positions[j].value),1);
    }else{
      this.selectedPositions[i].push(this.positions[j].value);
    }
  }

  updateTurn(){
    this.error=null;
    if (this.datesAndTurns.valid){
      let newPos={};
      let date = new Date(this.datesAndTurns.controls.date.value);
      for (let i = 0; i<this.datesAndTurns.value.turns.length; i++){
        this.datesAndTurns.value.turns[i].date = date.toISOString().substring(0,10);
        this.datesAndTurns.value.turns[i]._id= this.data.turns[i]._id;
        for (let j = 0; j<this.selectedPositions[i].length;j++){
          let positions = this.selectedPositions[i];
          newPos[positions[j]] = this.pilots[j]._id;
          this.datesAndTurns.value.turns[i].positions=newPos;
        }
        newPos={}
      }
      let body ={};
      body = Object.assign({ turns: this.datesAndTurns.value.turns }, body);

      this.adminReservationsService.updateTurns(this.data._id,body).subscribe(
        res=>{
          this.dialogRef.close("La reservación se ha actualizado");
        },
        err=>{
          this.error= err;
        }
      )
    }else{
      this.datesAndTurns.updateValueAndValidity();
    }
  }
}