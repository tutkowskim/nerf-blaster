import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { JoystickComponent } from './joystick/joystick.component';
import { VideoFeedComponent } from './video-feed/video-feed.component';

@NgModule({
  declarations: [
    AppComponent,
    JoystickComponent,
    VideoFeedComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
