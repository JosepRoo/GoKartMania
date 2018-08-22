import { EditReservationDialogComponent } from './../edit-reservation-dialog/edit-reservation-dialog.component';
import { Component, OnInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatTableDataSource, MatDialog } from '@angular/material';

@Component({
  selector: 'app-reservation-details-dialog',
  templateUrl: './reservation-details-dialog.component.html',
  styleUrls: ['./reservation-details-dialog.component.scss']
})
export class ReservationDetailsDialogComponent implements OnInit {

  pilots;
  dataSourcePilots;
  displayedColumnsPilots: string[] = [
    'id',
    'name',
    'last_name',
    'nickname'
  ];

  turns;
  dataSourceTurns;
  displayedColumnsTurns:string[] =[
    'schedule',
    'turn_number',
    'positions'
  ];

  editReservationDialogRef;
  editAvailable;
  date;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialog: MatDialog
  ) { }

  ngOnInit() {
    this.date = this.data.reservation.date.substring(0,10);
    this.pilots = this.data.reservation.pilots;
    this.dataSourcePilots = new MatTableDataSource(this.pilots);
    this.turns = this.data.reservation.turns;
    this.editAvailable = this.data.parent == 'home'? 0 : 1;
    this.getPositions();
  }

  getPositions(){
    for (let turn of this.turns){
      turn.stringPositions = Object.keys(turn.positions);
      turn.stringPositions.join(', ');
    }
    this.dataSourceTurns = new MatTableDataSource(this.turns);

  }

  openEditReservationDialog(element) {
    this.editReservationDialogRef = this.dialog.open(EditReservationDialogComponent, {
      width: '90%',
      data : element.reservation,
      maxHeight: 800
    });
    this.editReservationDialogRef.afterClosed().subscribe(
      res=> {
        if (res!== ""){
          this.turns = res.turns;
          this.date = res.turns[0].date;
          this.getPositions();
        }
      }
    );
  }

}
