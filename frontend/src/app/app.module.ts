import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatMenuModule } from '@angular/material/menu';

import { AppComponent } from './app.component';
import { JoystickComponent } from './joystick/joystick.component';
import { VideoFeedComponent } from './video-feed/video-feed.component';
import { ControlPanelComponent } from './control-panel/control-panel.component';
import { AppRoutingModule } from './app-routing.module';
import { HomeComponent } from './home/home.component';
import { DebugComponent } from './debug/debug.component';

@NgModule({
  declarations: [
    AppComponent,
    JoystickComponent,
    VideoFeedComponent,
    ControlPanelComponent,
    HomeComponent,
    DebugComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatIconModule,
    MatToolbarModule,
    MatMenuModule,
    AppRoutingModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
