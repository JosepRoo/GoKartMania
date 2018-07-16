import { AdminService } from './admin/services/admin.service';
import { AdminReservationsService } from './admin/services/admin-reservations.service';
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
import { MatCardModule } from '@angular/material/card';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTableModule } from '@angular/material/table';

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
import { ReservationService } from './client/services/reservation.service';
import { DatesService } from './client/services/dates.service';
import { PromosService } from './admin/services/promos.service';

// Components
import { AppComponent } from './app.component';
import { ClientComponent } from './client/app.component';
import { ReservationComponent } from './client/reservation/reservation.component';
import { NavbarComponent } from './client/navbar/navbar.component';
import { InstructionsComponent } from './client/instructions/instructions.component';
import { FooterComponent } from './client/footer/footer.component';
import { PilotsComponent } from './client/pilots/pilots.component';
import { TurnComponent } from './client/turn/turn.component';
import { CalendarComponent } from './client/calendar/calendar.component';
import { PaymentComponent } from './client/payment/payment.component';
import { ConfirmComponent } from './client/confirm/confirm.component';
import { HomeComponent } from './admin/home/home.component';
import { AdminComponent } from './admin/app.component';
import { LogInComponent } from './log-in/log-in.component';
import { PromosComponent } from './admin/promos/promos.component';
import { ReservationsComponent } from './admin/reservations/reservations.component';

registerLocaleData(localeEs, 'es');

@NgModule({
  declarations: [
    AppComponent,
    ClientComponent,
    AdminComponent,
    ReservationComponent,
    NavbarComponent,
    InstructionsComponent,
    FooterComponent,
    PilotsComponent,
    TurnComponent,
    CalendarComponent,
    PaymentComponent,
    ConfirmComponent,
    HomeComponent,
    LogInComponent,
    PromosComponent,
    ReservationsComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatCheckboxModule,
    MatDatepickerModule,
    MatMomentDateModule,
    MatCardModule,
    MatBadgeModule,
    MatToolbarModule,
    MatIconModule,
    MatSelectModule,
    MatProgressSpinnerModule,
    MatRadioModule,
    MatDividerModule,
    MatTableModule,
    NgXCreditCardsModule,
    CalendarModule.forRoot(),
    MatSidenavModule,
    MDBBootstrapModule.forRoot(),
    AppRoutingModule
  ],
  schemas: [NO_ERRORS_SCHEMA],
  providers: [
    ReservationService,
    DatesService,
    PromosService,
    AdminReservationsService,
    AdminService,
    DatePipe,
    { provide: LOCALE_ID, useValue: 'es' }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
