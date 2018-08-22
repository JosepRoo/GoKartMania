import { Component, OnInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material';

@Component({
  selector: 'app-pilot-details-dialog',
  templateUrl: './pilot-details-dialog.component.html',
  styleUrls: ['./pilot-details-dialog.component.scss']
})
export class PilotDetailsDialogComponent implements OnInit {


  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any
  ) { }

  ngOnInit() {
  }

}
