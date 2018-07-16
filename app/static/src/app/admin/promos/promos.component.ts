import { PromosService } from './../services/promos.service';
import { Component, OnInit, ViewChild} from '@angular/core';
import { MatSort, MatTableDataSource } from '@angular/material';

@Component({
  selector: 'app-promos',
  templateUrl: './promos.component.html',
  styleUrls: ['./promos.component.scss']
})
export class PromosComponent implements OnInit {
  promos;
  displayedColumns: string[] = [
    'authorised',
    'type',
    'value',
    'existence',
    'start_date',
    'end_date',
    'actions'
  ];
  @ViewChild(MatSort) sort: MatSort;

  constructor(private promosService: PromosService) {}

  ngOnInit() {
    this.promosService.getPromos().subscribe(res => {
      this.promos = new MatTableDataSource(res);
      this.promos.sort = this.sort;
    });
  }
}
