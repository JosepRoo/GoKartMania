import { AdminService } from './../services/admin.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  busyHours;
  averagePrice;
  income;
  promos;
  displayedColumns: string[] = ['party_size', 'schedule'];
  constructor(private adminService: AdminService) {}

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
      console.log(res);
    });
  }
}
