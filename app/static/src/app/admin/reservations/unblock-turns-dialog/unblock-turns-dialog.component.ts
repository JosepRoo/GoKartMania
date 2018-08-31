import { Component, OnInit, Inject } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { AdminService } from '../../services/admin.service';

@Component({
  selector: 'app-unblock-turns-dialog',
  templateUrl: './unblock-turns-dialog.component.html',
  styleUrls: ['./unblock-turns-dialog.component.scss']
})
export class UnblockTurnsDialogComponent implements OnInit {

  unblockedTurns: FormGroup;
  error;
  allDay: Boolean = false;

  schedules: string[] = ['11','12','13','14','15','16','17','18','19','20','21'];
  turns: number[] = [1,2,3,4,5]
  
  constructor(
    private _formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<UnblockTurnsDialogComponent>,
    private adminService: AdminService,
    @Inject(MAT_DIALOG_DATA) private data: any,
  ) { 
    this.unblockedTurns = this._formBuilder.group({
      days:[[this.data.toISOString().substring(0,10)]],
      schedules:['',Validators.required],
      turns:['',Validators.required]
    });
  }

  ngOnInit() {
  }

  changeCheckbox(isChecked){
    if (isChecked){
      this.unblockedTurns.controls.schedules.setValue(this.schedules);
      this.unblockedTurns.controls.turns.setValue(this.turns);
    }else{
      this.unblockedTurns.controls.schedules.setValue([]);
      this.unblockedTurns.controls.turns.setValue([]);
    }
  }

  unblockTurns(){
    this.adminService.unblockTurns(this.unblockedTurns.getRawValue()).subscribe(
      res=>{
        this.dialogRef.close();
      },
      err=>{
        this.error = err;
      }
    )
  }
}
