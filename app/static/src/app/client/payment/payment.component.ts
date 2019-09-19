import { MatDialog } from '@angular/material';
import { ReservationService } from '../services/reservation.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {
  Component,
  OnInit,
  Output,
  EventEmitter,
  ElementRef,
  ViewChild,
  OnDestroy
} from '@angular/core';
import { CreditCardValidator } from 'ngx-credit-cards';
import { DeleteTurnDialogComponent } from './delete-turn-dialog/delete-turn-dialog.component';

@Component({
  selector: 'app-payment',
  templateUrl: './payment.component.html',
  styleUrls: ['./payment.component.scss']
})
export class PaymentComponent implements OnInit, OnDestroy {
  loading: Boolean = false;
  payment: FormGroup;
  promo = {
    error: false,
    promo_id: ''
  };
  reservation;
  error = {
    show: false,
    text: ''
  };

  today = new Date();
  years = [];

  @Output() goBack: EventEmitter<any> = new EventEmitter<any>();
  @ViewChild('pilotFormButton') pilotFormButton: ElementRef;
  @Output() paymentDone: EventEmitter<any> = new EventEmitter<any>();

  deleteTurnDialogRef;

  constructor(
    private formBuilder: FormBuilder,
    private reservationService: ReservationService,
    private dialog: MatDialog
  ) {}

  ngOnInit() {

    let year = this.today.getFullYear();
    for (let i = 0; i < 7; i++) {
      this.years.push(year);
      year = year + 1;
    }
    console.log(this.years);

    this.getReservation();
    this.payment = this.formBuilder.group({
      payment_method: ['', Validators.required],
      name: ['', Validators.required],
      number: [
        '',
        [Validators.required, CreditCardValidator.validateCardNumber]
      ],
      month: ['', Validators.required],
      year: ['', Validators.required],
      cvv: ['', [Validators.required, CreditCardValidator.validateCardCvc]],
      promo_id: [],
      coupon_id: [],
      payment_type: ['Etomin', Validators.required],
      user_name: ['', Validators.required],
      user_email: ['', [Validators.required, Validators.email]],
      user_id: [],
      phone: ['', [Validators.required, Validators.pattern('[0-9]{10}') ]]
    });
  }

  ngOnDestroy(){
    if(this.deleteTurnDialogRef){
      this.deleteTurnDialogRef.close();
    }
  }

  applyPromo() {
    const self = this;
    this.promo.error = false;
    this.reservationService.putPromo(this.promo).subscribe(
      res => {
        this.reservation = res;
        this.payment.controls.promo_id.setValue(res.promo_id);
        this.payment.controls.coupon_id.setValue(res.coupon_id);
      },
      _error => {
        this.promo.error = true;
        self.reservationService.getReservation().subscribe(res => {
          self.reservation = res;
          self.payment.controls.promo_id.setValue(null);
          self.payment.controls.coupon_id.setValue(null);
        });
      }
    );
  }

  sendPayment() {
    const self = this;
    if (this.payment.valid) {
      this.loading = true;
      const user = {
        name: this.payment.controls.user_name.value,
        email: this.payment.controls.user_email.value
      };
      this.reservationService.postUser(user).subscribe(
        res => {
            // // TODO remove om prod
            // self.paymentDone.emit();
          self.payment.controls.user_id.setValue(res._id);
          self.reservationService
            .postPayment(self.payment.getRawValue())
            .subscribe(
              _pay => {
                this.loading = false;
                self.paymentDone.emit();
              },
              error => {
                self.error.show = true;
                self.error.text = error;
                this.loading = false;
              }
            );
        },
        error => {
          self.error.show = true;
          self.error.text = error;
          this.loading = false;
        }
      );
    }
  }

  submitPayment() {
    this.pilotFormButton.nativeElement.click();
  }

  getReservation(){
    this.reservationService.getReservation().subscribe(res => {
      this.reservation = res;
      this.reservation.date = new Date(this.reservation.date.replace(/-/g, '/'));
    });
  }

  deleteTurn(turn, date){
    this.deleteTurnDialogRef = this.dialog.open(DeleteTurnDialogComponent,{
      width: '70%',
      data:{
        turn:turn,
        date: date
      }
    });

    this.deleteTurnDialogRef.afterClosed().subscribe(
			()=>{
        this.getReservation();
      }
		);
  }
}
