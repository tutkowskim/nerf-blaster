import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NerfBlasterService {
  // TODO: get initial values from backend
  private _horizotnalAngle: number = 0;
  private _verticalAngle: number = 0;

  constructor(private http: HttpClient) { }

  public get horizontalAngle(): number {
    return this._horizotnalAngle;
  }

  public setHorizontalAngle(value: number): void {
    firstValueFrom(this.http.post<number>('/api/set_horizontal_angle', value)).then((value) => this._horizotnalAngle = value);
  }

  public get verticalAngle(): number {
    return this._verticalAngle;
  }

  public setVerticalAngle(value: number): void {
    firstValueFrom(this.http.post<number>('/api/set_vertical_angle', value)).then((value) => this._verticalAngle = value);
  }
}
