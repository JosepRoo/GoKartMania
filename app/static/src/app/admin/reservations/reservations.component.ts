import { DeleteReservationDialogComponent } from './delete-reservation-dialog/delete-reservation-dialog.component';
import { AdminService } from './../services/admin.service';
import { BlockTurnsDialogComponent } from './block-turns-dialog/block-turns-dialog.component';
import { AdminDatesService } from './../services/admin-dates.service';
import { CreateReportDialogComponent } from './create-report-dialog/create-report-dialog.component';
import { EditReservationDialogComponent } from './edit-reservation-dialog/edit-reservation-dialog.component';
import { MatTableDataSource, MatSort, MatDialog, MatIconRegistry } from '@angular/material';
import { AdminReservationsService } from './../services/admin-reservations.service';
import { Component, OnInit, ViewChild, OnDestroy } from '@angular/core';
import { NewReservationDialogComponent } from './new-reservation-dialog/new-reservation-dialog.component';
import { DomSanitizer } from '@angular/platform-browser';
import { ReservationDetailsDialogComponent } from './reservation-details-dialog/reservation-details-dialog.component';

import { CalendarComponent } from '../../client/calendar/calendar.component';
import { DatePipe } from '@angular/common';
import { SelectionModel } from '@angular/cdk/collections';

@Component({
  selector: 'app-reservations',
  templateUrl: './reservations.component.html',
  styleUrls: ['./reservations.component.scss']
})
export class ReservationsComponent implements OnInit, OnDestroy {

  reservations; 
  dataSourceReservations;
  dataSourceBlockedTurns;
  defaultDate = new Date();
  newReservationDialogRef;
  editReservationDialogRef;
  createReportDialogRef;
  reservationDetailsDialogRef;
  blockTurnsDialogRef;
  deleteReservationDialogRef;
  @ViewChild(MatSort) sort: MatSort;
  @ViewChild(CalendarComponent) calendar: CalendarComponent;
  calendarMode:string;
  select =false;

  displayedColumnsReservations: string[] = [
    'location',
    'type',
    'date',
    'hour',
    'turn',
    'total_price',
    'edit',
    'delete'
  ];

  // displayedColumnsBlockedTurns: string[] = [
  //   'schedule',
  //   'turn',

  // ]

  startDate:Date;
  endDate:Date;

  availableDates: Array<any>;
  selectedDay: Date;
  preventBack = true;
  mode:string = "normal";
  blockedDates = [];
  error: string;
  selectedDate;
  blockedTurns = [];
  selection;

  constructor(
    private reservationService: AdminReservationsService,
    private dialog: MatDialog,
    private iconRegistry: MatIconRegistry,
    private sanitizer: DomSanitizer,
    private datesService: AdminDatesService,
    private datePipe: DatePipe,
    private adminService: AdminService
  ) {
    this.iconRegistry
    .addSvgIcon('icn_edit', this.sanitizer.bypassSecurityTrustResourceUrl('../../assets/edit.svg'));
   }

  ngOnInit() {
    this.calendarMode = 'normal';
    const now = new Date();
    this.setDateRange(now.getFullYear(), now.getMonth(), now.getDate());
    this.getAvailableDates();
  }

  ngOnDestroy() {
    if (this.newReservationDialogRef) {
      this.newReservationDialogRef.close();
    }
    if (this.editReservationDialogRef) {
      this.editReservationDialogRef.close();
    }
    if (this.createReportDialogRef) {
      this.createReportDialogRef.close();
    }
    if (this.reservationDetailsDialogRef) {
      this.reservationDetailsDialogRef.close();
    }
    if (this.blockTurnsDialogRef) {
      this.blockTurnsDialogRef.close();
    }
    if(this.deleteReservationDialogRef){
      this.deleteReservationDialogRef.close();
    }
  }

  openNewReservationDialog() {
    this.newReservationDialogRef = this.dialog.open(NewReservationDialogComponent, {
      width: '60%',
      maxHeight: 700,
    });
  }

  openEditReservationDialog(element) {
    this.editReservationDialogRef = this.dialog.open(EditReservationDialogComponent, {
      width: '60%',
      data : element,
      maxHeight: 800
    });

  }

  openCreateReportDialog() {
    this.createReportDialogRef = this.dialog.open(CreateReportDialogComponent, {
      width: '60%',
    });
  }

  openDeleteReservationDialog(element){
    this.deleteReservationDialogRef = this.dialog.open(DeleteReservationDialogComponent,{
      width:'70%',
      data: element
    });
    this.deleteReservationDialogRef.afterClosed().subscribe(
    ()=>{
      this.getReservations(this.selectedDate);
    }
    )
  }

  getReservations(date) {
    let startDate = date.toISOString().substring(0,10);
    this.reservationService.getUpcomingReservations(startDate,startDate).subscribe(res => {
      this.dataSourceReservations = new MatTableDataSource(res);
      this.dataSourceReservations.sort = this.sort;
    });
  }

  // getBlockedTurns(selectedDate){
  //   this.blockedTurns=[];
  //   let date = selectedDate.toISOString().substring(0,10);
  //   this.adminService.getBlockedTurns(date).subscribe(
  //     res=>{
  //       this.selection = new SelectionModel<any>(true, []);
  //       console.log(res);
  //       for (let i = 0; i<res.schedules.length;i++){
  //         for (let j = 0; j < res.turns.length; j ++){
  //           this.blockedTurns.push ({'schedule':res.schedules[i], 'turn':res.turns[j]});
  //         }
  //       }
  //       console.log(this.blockedTurns);
  //       this.dataSourceBlockedTurns = new MatTableDataSource(this.blockedTurns);
  //     }
  //   )
  // }

  openReservationDetail(reservation){
    this.reservationDetailsDialogRef = this.dialog.open(ReservationDetailsDialogComponent,{
      width:'60%',
      maxHeight:600,
      data:{
        reservation: reservation,
        parent: 'reservation'
      }
    });

    this.reservationDetailsDialogRef.afterClosed().subscribe(()=>{
      this.getAvailableDates();
      this.getReservations(this.selectedDate);
      // this.getBlockedTurns(this.selectedDate);
    })
  }

  setDateRange(year, month, day) {
    const date = new Date(year, month, day);
    const daysMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0);
    this.startDate = new Date(
      date.getFullYear(),
      date.getMonth(),
      date.getDate()
    );
    this.endDate = new Date(
      date.getFullYear(),
      date.getMonth(),
      daysMonth.getDate()
    );
  }

  getAvailableDates() {
    this.datesService
      .getAvailableDates(
        this.datePipe.transform(this.startDate, 'yyyy-MM-dd'),
        this.datePipe.transform(this.endDate, 'yyyy-MM-dd')
      )
      .subscribe(
        (res: Array<any>) => {
          res.map(
            el => {
              el.fecha = new Date(el.date);
            },
            error => {
              {
              }
            }
          );
          this.availableDates = res;
          if(this.calendar){
            this.calendar.availableDates = res;
            this.calendar.reRender();
          }
        }
      );
  }

  onSelectedDate(date, flag) {
    this.selectedDate = date;
    if(this.mode === "normal"){
      this.blockedDates=[];
      this.blockedDates.push(date.toISOString().substring(0,10));
      this.getReservations(date);
      // this.getBlockedTurns(date);
    }else if(this.mode ==="block"){
      if(!this.blockedDates.includes(date)){
        this.blockedDates.push(date);
      }else{
        this.blockedDates.splice(this.blockedDates.indexOf(date),1);
      }
    }
    
  }

  onDateChange(date: Date) {
    const now = new Date();
    this.preventBack =
      now.getFullYear() === date.getFullYear() &&
      now.getMonth() === date.getMonth();
    this.setDateRange(date.getFullYear(), date.getMonth(), date.getDate());
    this.availableDates = null;
    this.getAvailableDates();
  }

  blockTurns(){
    this.error = null;
    if(this.blockedDates.length === 0){
      this.error = "No has seleccionado ningún día";
      this.closeBanner();
    }else{
      this.blockTurnsDialogRef = this.dialog.open(BlockTurnsDialogComponent,{
        width:'40%',
        data: this.blockedDates
      })
      this.blockTurnsDialogRef.afterClosed().subscribe(()=>{
        this.blockedDates = [];
        this.changeMode();
      })
    }
    
  }

  changeMode(){
    if (this.mode === "normal"){
      this.mode = "block";
    }else{
      this.mode = "normal";
      this.calendar.reRender();
    }
  }

  // unblockTurns(){
  //   this.select = !this.select;

  //   if(this.select){
  //     this.displayedColumnsBlockedTurns.push('select');
  //   }else{
  //     // this.adminService.unblockTurns().subscribe(
  //     //   res=>{

  //     //   }
  //     // )
  //     this.displayedColumnsBlockedTurns.splice(this.displayedColumnsBlockedTurns.length-1,1);
  //   }
  // }

  closeBanner(){
    setTimeout(()=>{
      this.error = null;
    },8000);
  }

  // isAllSelected() {
  //   const numSelected = this.selection.selected.length;
  //   const numRows = this.dataSourceReservations.data.length;
  //   return numSelected === numRows;
  // }

  // masterToggle() {
  //   this.isAllSelected() ?
  //       this.selection.clear() :
  //       this.dataSourceReservations.data.forEach(row => this.selection.select(row));
  // }
}