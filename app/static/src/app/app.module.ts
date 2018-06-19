import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing';

// Material Design
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

// Boostrap
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { MDBBootstrapModule } from 'angular-bootstrap-md';

// Dependencies
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { ReservationComponent } from './reservation/reservation.component';
import { NavbarComponent } from './navbar/navbar.component';
import { InstructionsComponent } from './instructions/instructions.component';
import { FooterComponent } from './footer/footer.component';


@NgModule({
  declarations: [
    AppComponent,
    ReservationComponent,
    NavbarComponent,
    InstructionsComponent,
    FooterComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    MDBBootstrapModule.forRoot()
  ],
  schemas: [ NO_ERRORS_SCHEMA ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
