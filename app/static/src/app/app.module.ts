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
import { MatDialogModule } from '@angular/material/dialog';
import { MatStepperModule } from '@angular/material/stepper';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatSortModule } from '@angular/material';

// Calendar
import { CalendarModule } from 'angular-calendar';

// Bootstrap
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { MDBBootstrapModule } from 'angular-bootstrap-md';

// Dependencies
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

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
import { NewPromoDialogComponent } from './admin/promos/new-promo-dialog/new-promo-dialog.component';
import { EditPromoDialogComponent } from './admin/promos/edit-promo-dialog/edit-promo-dialog.component';
import { AdminPilotsComponent } from './admin/admin-pilots/admin-pilots.component';
import { NewReservationDialogComponent } from './admin/reservations/new-reservation-dialog/new-reservation-dialog.component';
import { EditReservationDialogComponent } from './admin/reservations/edit-reservation-dialog/edit-reservation-dialog.component';
import { CreateReportDialogComponent } from './admin/reservations/create-report-dialog/create-report-dialog.component';
import { LogoutDialogComponent } from './admin/logout-dialog/logout-dialog.component';
import { PromoDetailsDialogComponent } from './admin/promos/promo-details-dialog/promo-details-dialog.component';
import { PilotDetailsDialogComponent } from './admin/admin-pilots/pilot-details-dialog/pilot-details-dialog.component';
import { ReservationDetailsComponent } from './admin/reservations/reservation-details/reservation-details.component';
import { ReservationDetailsDialogComponent } from './admin/reservations/reservation-details-dialog/reservation-details-dialog.component';
import { PilotsLicensesComponent } from './admin/pilots-licenses/pilots-licenses.component';
import { BlockTurnsDialogComponent } from './admin/reservations/block-turns-dialog/block-turns-dialog.component';
import { DeleteTurnDialogComponent } from './client/payment/delete-turn-dialog/delete-turn-dialog.component';
import { AdminsComponent } from './admin/admins/admins.component';
import { EditAdminDialogComponent } from './admin/admins/edit-admin-dialog/edit-admin-dialog.component';
import { DeleteAdminDialogComponent } from './admin/admins/delete-admindialog/delete-admindialog.component';
import { NewAdminDialogComponent } from './admin/admins/new-admin-dialog/new-admin-dialog.component';
import { DeleteReservationDialogComponent } from './admin/reservations/delete-reservation-dialog/delete-reservation-dialog.component';
import { UnblockTurnsDialogComponent } from './admin/reservations/unblock-turns-dialog/unblock-turns-dialog.component';

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
    ReservationsComponent,
    NewPromoDialogComponent,
    EditPromoDialogComponent,
    AdminPilotsComponent,
    NewReservationDialogComponent,
    EditReservationDialogComponent,
    CreateReportDialogComponent,
    LogoutDialogComponent,
    PromoDetailsDialogComponent,
    PilotDetailsDialogComponent,
    ReservationDetailsComponent,
    ReservationDetailsDialogComponent,
    PilotsLicensesComponent,
    BlockTurnsDialogComponent,
    DeleteTurnDialogComponent,
    AdminsComponent,
    EditAdminDialogComponent,
    DeleteAdminDialogComponent,
    NewAdminDialogComponent,
    DeleteReservationDialogComponent,
    UnblockTurnsDialogComponent
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
    MatDialogModule,
    MatStepperModule,
    MatGridListModule,
    CalendarModule.forRoot(),
    MatSidenavModule,
    MDBBootstrapModule.forRoot(),
    AppRoutingModule,
    MatSortModule
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
  bootstrap: [AppComponent],
  entryComponents: [
    NewPromoDialogComponent,
    EditPromoDialogComponent,
    NewReservationDialogComponent,
    EditReservationDialogComponent,
    CreateReportDialogComponent,
    LogoutDialogComponent,
    PromoDetailsDialogComponent,
    PilotDetailsDialogComponent,
    ReservationDetailsDialogComponent,
    BlockTurnsDialogComponent,
    DeleteTurnDialogComponent,
    EditAdminDialogComponent,
    DeleteAdminDialogComponent,
    NewAdminDialogComponent,
    DeleteReservationDialogComponent,
    UnblockTurnsDialogComponent
  ]
})
export class AppModule {}
