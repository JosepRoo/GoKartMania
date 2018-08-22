import { MatTableDataSource } from '@angular/material/table';
import { AdminReservationsService } from './../../services/admin-reservations.service';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-reservation-details',
  templateUrl: './reservation-details.component.html',
  styleUrls: ['./reservation-details.component.scss']
})
export class ReservationDetailsComponent implements OnInit {

  id;
  reservation;
  error;
  display;

  dataSourcePilots;
  dataSourceTurns;
  displayedColumnsPilots: string[] = [
    'id',
    'name',
    'last_name',
    'nickname'
  ];
  displayedColumnsTurns:string[] =[
    'schedule',
    'turn_number',
    'positions'
  ];

  constructor(
    private route: ActivatedRoute,
    private reservationsService: AdminReservationsService
  ) {
    this.id = this.route.snapshot.params['id'];
   }

  ngOnInit() {
    this.display = false;
    this.getReservation();
  }

  getReservation(){
    this.reservationsService.getReservation(this.id).subscribe(
      res=>{
        this.reservation = res;
        this.dataSourcePilots = new MatTableDataSource(this.reservation.pilots);
        for (let turn of this.reservation.turns){
          turn.stringPositions = Object.keys(turn.positions);
          turn.stringPositions.join(', ');
        }
        this.dataSourceTurns = new MatTableDataSource(this.reservation.turns);
        this.display = true;
      },
      err=>{
        this.error = err;
      }
    )
  }
}
