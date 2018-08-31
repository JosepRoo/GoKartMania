import { AdminReservationsService } from './../../services/admin-reservations.service';
import { Component, OnInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { AdminService } from '../../services/admin.service';

@Component({
  selector: 'app-delete-reservation-dialog',
  templateUrl: './delete-reservation-dialog.component.html',
  styleUrls: ['./delete-reservation-dialog.component.scss']
})
export class DeleteReservationDialogComponent implements OnInit {

  constructor(
    private dialogRef: MatDialogRef<DeleteReservationDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private reservationService: AdminReservationsService
  ) { }

  ngOnInit() {
  }

  deleteReservation(){
    this.reservationService.deleteReservation(this.data._id).subscribe(
      res=>{
        this.dialogRef.close();
      },
      err=>{
        this.dialogRef.close(err);
      }
    )
  }
}
