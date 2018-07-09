import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.scss']
})
export class ReservationComponent implements OnInit {
  state: String;
  reservation: {
    id_location: Number;
    type: String;
    pilots: Array<{}>;
    date: Date;
  };
  stages = ['pilots', 'turns'];
  selectedStage = 1;

  constructor() {
    this.state = this.stages[this.selectedStage];
  }

  ngOnInit() {
    this.reservation = {
      type: 'Adultos',
      id_location: 1,
      pilots: [],
      date: null
    };
  }

  getReservation(reservation) {
    this.reservation = reservation;
    this.goForward();
  }

  goForward() {
    this.selectedStage = this.selectedStage + 1;
    this.state = this.stages[this.selectedStage];
  }

  goBackward() {
    this.selectedStage = this.selectedStage - 1;
    this.state = this.stages[this.selectedStage];
  }
}
