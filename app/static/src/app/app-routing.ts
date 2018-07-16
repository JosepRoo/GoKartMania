import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Components
import { ReservationComponent } from './client/reservation/reservation.component';
import { InstructionsComponent } from './client/instructions/instructions.component';
import { ClientComponent } from './client/app.component';
import { HomeComponent } from './admin/home/home.component';

export const routes: Routes = [
  {
    path: '',
    component: ClientComponent,
    children: [
      {
        path: 'instrucciones',
        component: InstructionsComponent
      },
      {
        path: 'reservar',
        component: ReservationComponent
      },
      {
        path: '',
        redirectTo: '/instrucciones',
        pathMatch: 'full'
      },
      {
        path: '**', redirectTo: 'instrucciones'
      }
    ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
    exports: [RouterModule]
})
export class AppRoutingModule { }
