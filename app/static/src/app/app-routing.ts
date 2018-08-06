import { LogInComponent } from './log-in/log-in.component';
import { AdminComponent } from './admin/app.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Components
import { ReservationComponent } from './client/reservation/reservation.component';
import { InstructionsComponent } from './client/instructions/instructions.component';
import { ClientComponent } from './client/app.component';
import { HomeComponent } from './admin/home/home.component';
import { PromosComponent } from './admin/promos/promos.component';
import { ReservationsComponent } from './admin/reservations/reservations.component';
import { AdminPilotsComponent } from './admin/admin-pilots/admin-pilots.component';

export const routes: Routes = [
  {
    path: 'admin',
    component: AdminComponent,
    children: [
      {
        path: '',
        component: HomeComponent
      },
      {
        path: 'home',
        component: HomeComponent
      },
      {
        path: 'promos',
        component: PromosComponent
      },
      {
        path: 'pilots',
        component: AdminPilotsComponent
      },
      {
        path: 'reservations',
        component: ReservationsComponent
      },
      {
        path: '',
        redirectTo: '/home',
        pathMatch: 'full'
      },
      {
        path: '**', redirectTo: 'home'
      }
    ]
  },
  {
    path: 'logIn',
    component: LogInComponent,
  },
  {
    path: '',
    component: ClientComponent,
    children: [
      {
        path: '',
        component: InstructionsComponent
      },
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
  {
    path: '',
    redirectTo: '',
    pathMatch: 'full'
  },
  {
    path: '**', redirectTo: ''
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
    exports: [RouterModule]
})
export class AppRoutingModule { }
