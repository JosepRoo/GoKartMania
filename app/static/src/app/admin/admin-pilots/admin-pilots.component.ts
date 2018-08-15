import { Component, OnInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { AdminPilotsService } from '../services/admin-pilots.service';
import { MatDialog } from '@angular/material';
import { PilotDetailsDialogComponent } from './pilot-details-dialog/pilot-details-dialog.component';

@Component({
  selector: 'app-admin-pilots',
  templateUrl: './admin-pilots.component.html',
  styleUrls: ['./admin-pilots.component.scss']
})
export class AdminPilotsComponent implements OnInit {

  pilots;
  dataSourcePilots;

  pilotDetailsDialogRef;

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
      console.log(res);
      this.pilots = res;
      this.dataSourcePilots = new MatTableDataSource(this.pilots);
    });
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
