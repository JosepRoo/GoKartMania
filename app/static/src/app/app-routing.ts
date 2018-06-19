import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Componnents
import { ReservationComponent } from './reservation/reservation.component';
import { InstructionsComponent } from './instructions/instructions.component';

export const routes: Routes = [
  {
    path: 'instrucciones',
    component: InstructionsComponent
  },
  {
    path: 'reservar',
    component: ReservationComponent
  },
  {
    path: '**', redirectTo: 'instrucciones'
  }
];

@NgModule({
    imports: [RouterModule.forRoot(routes, {useHash: true})],
    exports: [RouterModule]
})
export class AppRoutingModule { }
