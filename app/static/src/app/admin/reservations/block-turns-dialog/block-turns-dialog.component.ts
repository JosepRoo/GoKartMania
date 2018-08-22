import { AdminService } from './../../services/admin.service';
import { Component, OnInit, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-block-turns-dialog',
  templateUrl: './block-turns-dialog.component.html',
  styleUrls: ['./block-turns-dialog.component.scss']
})
export class BlockTurnsDialogComponent implements OnInit {

  blockedTurns: FormGroup;
  error;
  allDay: Boolean = false;

  schedules: string[] = ['11','12','13','14','15','16','17','18','19','20','21'];
  turns: number[] = [1,2,3,4,5]
  constructor(
    private _formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<BlockTurnsDialogComponent>,
    private adminService: AdminService,
    @Inject(MAT_DIALOG_DATA) private data: any,
  ) {
    this.blockedTurns = this._formBuilder.group({
      days:[this.data],
      schedules:['',Validators.required],
      turns:['',Validators.required]
    });
   }

  ngOnInit() {
  }

  changeCheckbox(isChecked){
    if (isChecked){
      this.blockedTurns.controls.schedules.setValue(this.schedules);
      this.blockedTurns.controls.turns.setValue(this.turns);
    }else{
      this.blockedTurns.controls.schedules.setValue([]);
      this.blockedTurns.controls.turns.setValue([]);
    }
  }

  blockTurns(){
    this.adminService.blockTurns(this.blockedTurns.getRawValue()).subscribe(
      res=>{
        this.dialogRef.close();
      },
      err=>{
        this.error = err;
      }
    )
  }
}