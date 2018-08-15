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

  constructor(
    @Inject(MAT_DIALOG_DATA) private data: any,
    private dialog: MatDialog
  ) { }

  ngOnInit() {
    console.log(this.data);
    this.pilots = this.data.pilots;
    this.dataSourcePilots = new MatTableDataSource(this.pilots);
    this.turns = this.data.turns;
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
      data : element,
      maxHeight: 800
    });
    this.editReservationDialogRef.afterClosed().subscribe(
      res=> {
        this.turns = res.turns;
        this.getPositions();
      }
    );
  }

}
