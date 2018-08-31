import { Component, OnInit, ViewChild, OnDestroy } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { AdminPilotsService } from '../services/admin-pilots.service';
import { MatDialog, MatSort } from '@angular/material';
import { PilotDetailsDialogComponent } from './pilot-details-dialog/pilot-details-dialog.component';

@Component({
  selector: 'app-admin-pilots',
  templateUrl: './admin-pilots.component.html',
  styleUrls: ['./admin-pilots.component.scss']
})
export class AdminPilotsComponent implements OnInit, OnDestroy {

  pilots;
  dataSourcePilots;

  pilotDetailsDialogRef;

  @ViewChild(MatSort) sort: MatSort;

  displayedColumns: string[] = [
    'name',
    'last_name',
    'checked'
  ];
  error;

  constructor(
    private pilotsService: AdminPilotsService,
    private dialog: MatDialog
  ) { }

  ngOnInit() {
    this.pilotsService.getPilots().subscribe(res => {
      this.pilots = res;
      this.dataSourcePilots = new MatTableDataSource(this.pilots);
      this.dataSourcePilots.sort = this.sort;
    });
  }

  ngOnDestroy(){
    if(this.pilotDetailsDialogRef){
      this.pilotDetailsDialogRef.close();
    }
  }

  downloadDB(){
    this.pilotsService.generateReport();
  }

  openPilotDetail(pilot){
    this.pilotDetailsDialogRef = this.dialog.open(PilotDetailsDialogComponent,{
      width: '80%',
      data: pilot
    })
  }

}
