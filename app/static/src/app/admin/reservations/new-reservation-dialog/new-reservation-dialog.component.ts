import { AdminPilotsService } from './../../services/admin-pilots.service';
import { FormGroup, FormBuilder, FormArray, Validators } from '@angular/forms';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { AdminDatesService } from '../../services/admin-dates.service';
import { AdminReservationsService } from '../../services/admin-reservations.service';
import { MatStepper } from '@angular/material/stepper';

@Component({
  selector: 'app-new-reservation-dialog',
  templateUrl: './new-reservation-dialog.component.html',
  styleUrls: ['./new-reservation-dialog.component.scss']
})
export class NewReservationDialogComponent implements OnInit {

  @ViewChild('stepper') stepper: MatStepper;

  error;

  reservationData: FormGroup;
  datesAndTurns:FormGroup;
  user: FormGroup;

  minBirthDayDate = new Date(1920, 1, 1);
  today = new Date();
  maxReservationDate = new Date(new Date(this.today).setMonth(this.today.getMonth()+3))

  availableDates;
  availableSchedules;
  availableTurns;
  availablePositions;

  pilots;
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
    private _formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<NewReservationDialogComponent>,
    private adminDatesService: AdminDatesService,
    private adminReservationService: AdminReservationsService,
    private adminPilotsService: AdminPilotsService
  ) {
    this.reservationData = this._formBuilder.group({
      location:['',[Validators.required]],
      id_location:[1, Validators.required],
      type:['',[Validators.required]],
      pilots: this._formBuilder.array([])
    });
    
    this.datesAndTurns = this._formBuilder.group({
      date:['',Validators.required],
      schedule:['',Validators.required],
      turn_number:['',Validators.required],
      positions:[{}]
    });

    this.user = this._formBuilder.group({
      name:['',Validators.required],
      email:['',[Validators.required,Validators.email]],
    })
   }

  ngOnInit() {
  }

  createPilot(): FormGroup{
    return this._formBuilder.group({
      name:['',[Validators.required]],
      last_name:['',[Validators.required]],
      email:['',[Validators.required,Validators.email]],
      nickname:['',[Validators.required]],
      birth_date:['',[Validators.required]],
      postal_code:['',[Validators.required, Validators.pattern('[0-9]{5}')]],
      city:['',[Validators.required]],
      licensed:[true],
      buy_license:[false],
      location:[this.reservationData.controls.location.value]
    });
  }

  getFormData(){
    return this.reservationData.get('pilots') as FormGroup;
  }

  addPilot(){
    const pilots = this.reservationData.get('pilots') as FormArray
    if(this.reservationData.controls.type.value && pilots.length<8){
      pilots.push(this.createPilot());
    }
  }

  deletePilot(index) {
    const pilots = this.reservationData.get('pilots') as FormArray;
    pilots.removeAt(index);
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

  registerPilots(){
    if(this.reservationData.valid){
      if(this.validateAge()){
        this.adminReservationService.addReservation(this.reservationData.getRawValue()).subscribe(
          res=>{
            let pilots = this.reservationData.getRawValue().pilots;
            for (let pilot of pilots){
              pilot.birth_date = pilot.birth_date.toISOString().substring(2,10);
            }
            this.adminPilotsService.registerPilots(pilots).subscribe(
              res=>{
                this.pilots = res;
              },
              err=>{
                this.error = err;
              }
            )
          },
          err=>{
            this.error = err;
          }
        );
        this.closeBanner();
        this.getAvailableDates();
        this.stepper.selectedIndex = 1;
      }else{
        this.error = "Alguno de los pilotos no tiene la edad adecuada para este grupo";
        this.closeBanner();
      }
    }else{
      this.reservationData.controls.pilots.reset();
      this.reservationData.updateValueAndValidity();
    }
    
  }

  validateAge() {
    const pilots = this.reservationData.get('pilots') as FormArray;
    const res = true;
    for (let i = 0; i < pilots.controls.length; i++) {
      const pilot = pilots.controls[i] as FormGroup;
      const timeDiff = Math.abs(Date.now() - pilot.controls.birth_date.value);
      const age = Math.floor(timeDiff / (1000 * 3600 * 24) / 365);
      if (
        (this.reservationData.controls.type.value === 'Niños' &&
          (age < 5 || age > 12)) ||
        (this.reservationData.controls.type.value === 'Adultos' && age < 12)
      ) {
          return false;
        }
        return res;
    }
  }

  getAvailableSchedules(date){
    this.datesAndTurns.controls.schedule.reset();
    this.datesAndTurns.controls.turn_number.reset();
    this.availablePositions=[];
    this.selectedPositions=[];
    this.adminDatesService.getAvailableSchedules(date.toISOString().substring(0,10)).subscribe(
      res=>{
        res = res[0].schedules;
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
    this.selectedPositions =[];
    this.availableTurns = this.availableSchedules.find(x=>x.schedule==schedule).turns;
    this.availableTurns = this.availableTurns.filter(turn=> {
      if(turn.status !== 0){
        return turn;
      }
    });
  }

  getAvailablePositions(turn){
    this.availablePositions = this.availableTurns.find(x=>x.turn ==turn).positions;
  }

  selectPosition(position){

    if(this.selectedPositions.includes(position)){
      this.selectedPositions.splice(this.selectedPositions.indexOf(position),1);
    }else{
      this.selectedPositions.push(position);
    }
  }

  createTurn(){
    this.error = null;
    if (this.datesAndTurns.valid && this.user.valid){
      let positions = {};
      for (let i=0; i<this.selectedPositions.length; i++){
        positions['pos'+this.selectedPositions[i]]=(this.pilots[i])._id;
      }
      this.datesAndTurns.controls.positions.setValue(positions);


      this.adminReservationService.addTurn(this.datesAndTurns.getRawValue()).subscribe(
        res=>{
          this.adminReservationService.getReservations().subscribe(
            res=>{
              this.adminReservationService.setUserToPay(this.user.getRawValue()).subscribe(
                res=>{
                  this.adminReservationService.payReservationAsAdmin(res._id).subscribe(
                    res=>{
                      this.dialogRef.close();
                    },
                    err=>{
                      this.error = err;
                    }
                  )
                },
                err=>{
                  this.error=err;
                }
              )
            },
            err=>{
              this.error=err;
            }
          )
        },
        err=>{
          this.error = err;
        }
      );
      this.closeBanner();
    }
  }

  closeBanner(){
    setTimeout(()=>{
			this.error = null;
		},13000);
  }
}