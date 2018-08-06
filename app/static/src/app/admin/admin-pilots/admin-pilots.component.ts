import { Component, OnInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { AdminPilotsService } from '../services/admin-pilots.service';

@Component({
  selector: 'app-admin-pilots',
  templateUrl: './admin-pilots.component.html',
  styleUrls: ['./admin-pilots.component.scss']
})
export class AdminPilotsComponent implements OnInit {

  pilots;
  dataSourcePilots;

  displayedColumns: string[] = [
    'name',
    'last_name',
    'checked'
  ];
  error;

  constructor(
    private pilotsService: AdminPilotsService
  ) { }

  ngOnInit() {
    this.pilotsService.getPilots().subscribe(res => {
      this.pilots = res;
      this.dataSourcePilots = new MatTableDataSource(res);
    });
  }

  downloadDB(){
    this.pilotsService.generateReport();
  }

}
