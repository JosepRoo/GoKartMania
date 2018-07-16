import { BrowserModule } from '@angular/platform-browser';
import { NgModule, LOCALE_ID } from '@angular/core';
import { AppRoutingModule } from './app-routing';
import { MatMomentDateModule } from '@angular/material-moment-adapter';
import { registerLocaleData, DatePipe } from '@angular/common';

import localeEs from '@angular/common/locales/es';

// Material Design
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFormFieldModule } from '@angular/material';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatBadgeModule } from '@angular/material/badge';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDividerModule } from '@angular/material/divider';
import { MatRadioModule } from '@angular/material/radio';

// Calendar
import { CalendarModule } from 'angular-calendar';

// Bootstrap
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { MDBBootstrapModule } from 'angular-bootstrap-md';

// Dependencies
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgXCreditCardsModule } from 'ngx-credit-cards';

// Services
import { ReservationService } from './services/reservation.service';
import { DatesService } from './services/dates.service';

// Components
import { AppComponent } from './app.component';
import { ReservationComponent } from './reservation/reservation.component';
import { NavbarComponent } from './navbar/navbar.component';
import { InstructionsComponent } from './instructions/instructions.component';
import { FooterComponent } from './footer/footer.component';
import { PilotsComponent } from './pilots/pilots.component';
import { TurnComponent } from './turn/turn.component';
import { CalendarComponent } from './calendar/calendar.component';
import { PaymentComponent } from './payment/payment.component';
import { ConfirmComponent } from './confirm/confirm.component';

registerLocaleData(localeEs, 'es');

@NgModule({
  declarations: [
    AppComponent,
    ReservationComponent,
    NavbarComponent,
    InstructionsComponent,
    FooterComponent,
    PilotsComponent,
    TurnComponent,
    CalendarComponent,
    PaymentComponent,
    ConfirmComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatCheckboxModule,
    MatDatepickerModule,
    MatMomentDateModule,
    MatBadgeModule,
    MatIconModule,
    MatSelectModule,
    MatProgressSpinnerModule,
    MatRadioModule,
    MatDividerModule,
    NgXCreditCardsModule,
    CalendarModule.forRoot(),
    MDBBootstrapModule.forRoot()
  ],
  schemas: [NO_ERRORS_SCHEMA],
  providers: [
    ReservationService,
    DatesService,
    DatePipe,
    { provide: LOCALE_ID, useValue: 'es' }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
