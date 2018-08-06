import { CreateReportDialogComponent } from './create-report-dialog/create-report-dialog.component';
import { EditReservationDialogComponent } from './edit-reservation-dialog/edit-reservation-dialog.component';
import { MatTableDataSource, MatSort, MatDialog, MatIconRegistry } from '@angular/material';
import { AdminReservationsService } from './../services/admin-reservations.service';
import { Component, OnInit, ViewChild, OnDestroy } from '@angular/core';
import { NewReservationDialogComponent } from './new-reservation-dialog/new-reservation-dialog.component';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-reservations',
  templateUrl: './reservations.component.html',
  styleUrls: ['./reservations.component.scss']
})
export class ReservationsComponent implements OnInit, OnDestroy {

  reservations;
  dataSourceReservations;
  defaultDate = new Date().toISOString().substring(0, 10);
  newReservationDialogRef;
  editReservationDialogRef;
  createReportDialogRef;
  @ViewChild(MatSort) sort: MatSort;

  displayedColumnsReservations: string[] = [
    'location',
    'type',
    'date',
    'hour',
    'turn',
    'total_price',
    'edit'
  ];

  constructor(
    private reservationService: AdminReservationsService,
    private dialog: MatDialog,
    private iconRegistry: MatIconRegistry,
    private sanitizer: DomSanitizer
  ) {
    this.iconRegistry
    .addSvgIcon('icn_edit', this.sanitizer.bypassSecurityTrustResourceUrl('../../assets/edit.svg'));
   }

  ngOnInit() {
    this.getReservations();
  }

  ngOnDestroy() {
    if (this.newReservationDialogRef) {
      this.newReservationDialogRef.close();
    }
    if (this.editReservationDialogRef) {
      this.editReservationDialogRef.close();
    }
  }

  openNewReservationDialog() {
    this.newReservationDialogRef = this.dialog.open(NewReservationDialogComponent, {
      width: '90%',
      maxHeight: 700,
    });
    this.newReservationDialogRef.afterClosed().subscribe(
      () => {
        this.getReservations();
      }
    );
  }

  openEditReservationDialog(element) {
    this.editReservationDialogRef = this.dialog.open(EditReservationDialogComponent, {
      width: '90%',
      data : element,
      maxHeight: 800
    });
    this.editReservationDialogRef.afterClosed().subscribe(
      () => {
        this.getReservations();
      }
    );
  }

  openCreateReportDialog() {
    this.createReportDialogRef = this.dialog.open(CreateReportDialogComponent, {
      width: '90%',
    });

  }

  getReservations() {
    this.reservationService.getUpcomingReservations(this.defaultDate).subscribe(res => {
      this.dataSourceReservations = new MatTableDataSource(res);
      this.dataSourceReservations.sort = this.sort;
    });
  }


}
