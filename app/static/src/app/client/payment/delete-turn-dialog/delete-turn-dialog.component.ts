import { ReservationService } from './../../services/reservation.service';
import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-delete-turn-dialog',
  templateUrl: './delete-turn-dialog.component.html',
  styleUrls: ['./delete-turn-dialog.component.scss']
})
export class DeleteTurnDialogComponent implements OnInit {

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<DeleteTurnDialogComponent>,
    private reservationService: ReservationService
  ) { }

  ngOnInit() {
    console.log(this.data)
  }

  deleteTurn(){
    let date = this.data.date.toISOString().substring(0,10)
    this.reservationService.deleteTurn(this.data.turn._id,date).subscribe(
      res=>{
        this.dialogRef.close();
      },
      err=>{
        this.dialogRef.close(err);
      }
    )
  }

}
