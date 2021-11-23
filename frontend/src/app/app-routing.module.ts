import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { DebugComponent } from './debug/debug.component'

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'debug', component: DebugComponent },
  { path: '**', redirectTo: 'home'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }