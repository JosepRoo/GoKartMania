import { AdminReservationsService } from './../services/admin-reservations.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-reservations',
  templateUrl: './reservations.component.html',
  styleUrls: ['./reservations.component.scss']
})
export class ReservationsComponent implements OnInit {

  reservations;
  displayedColumns: string[] = [
    'name',
    'last_name',
    'checked'
  ];

  constructor( private reservationService: AdminReservationsService) { }

  ngOnInit() {
    this.reservationService.getReservations().subscribe(res => {
      this.reservations = res;
      console.log(res);
    });
  }

}
