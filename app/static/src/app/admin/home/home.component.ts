import { AdminService } from './../services/admin.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { AdminReservationsService } from '../services/admin-reservations.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatDialog } from '@angular/material/dialog';
import { ReservationDetailsDialogComponent } from '../reservations/reservation-details-dialog/reservation-details-dialog.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {
  busyHours;
  averagePrice;
  income;
  promos;
  dataSourceReservations;
  reservationDetailsDialogRef;
  displayedColumns: string[] = ['party_size', 'schedule'];
  displayedColumnsReservations: string[] = [
    'location',
    'type',
    'date',
    'hour',
    'turn',
    'total_price',
  ]; 
  constructor(
    private adminService: AdminService,
    private reservationsService: AdminReservationsService,
    private dialog: MatDialog
  ) {}

  ngOnInit() {
    this.adminService.getBusyHours().subscribe(res => {
      this.busyHours = res;
    });
    this.adminService.getAveragePrice().subscribe(res => {
      this.averagePrice = res;
    });

    const date = new Date(),
      y = date.getFullYear(),
      m = date.getMonth();
    const firstDay = new Date(y, m, 1);
    const lastDay = new Date(y, m + 1, 0);

    this.adminService
      .getIncome(
        firstDay.toISOString().substring(0, 10),
        lastDay.toISOString().substring(0, 10)
      )
      .subscribe(res => {
        this.income = res;
      });

    this.adminService.getPromosIncome(
      firstDay.toISOString().substring(0, 10),
      lastDay.toISOString().substring(0, 10)
    ).subscribe(res => {
      this.promos = res;
    });

    this.reservationsService.
      getUpcomingReservations(
        date.toISOString().substring(0,10),
        date.toISOString().substring(0,10)
      )
      .subscribe(res=>{
        this.dataSourceReservations = new MatTableDataSource(res);
      })
  }

  ngOnDestroy(){
    if(this.reservationDetailsDialogRef){
      this.reservationDetailsDialogRef.close();
    }
  }

  openReservationDetail(reservation){
    this.reservationDetailsDialogRef = this.dialog.open(ReservationDetailsDialogComponent,{
      width:'70%',
      maxHeight:600,
      data:{
        reservation: reservation,
        parent: 'home'
      }
    });
  }
}
