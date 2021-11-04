import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'frontend';

  constructor(private http: HttpClient) {
  }

  public turnOnLed() {
    this.http.post('/api/led_on', {}).subscribe((data: any) => console.log(data));
  }

  public turnOffLed() {
    this.http.post('/api/led_off', {}).subscribe((data: any) => console.log(data));
  }
}
