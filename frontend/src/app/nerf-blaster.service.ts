import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { firstValueFrom, Observable, ReplaySubject } from 'rxjs';

interface StatusResult {
  cameraFps: number
  fireControllerStatus: string
  horizontalAngle: number
  verticalAngle: number
  trackingEnabled: boolean
}

@Injectable({
  providedIn: 'root'
})
export class NerfBlasterService {
  private readonly _cameraFps$: ReplaySubject<number> = new ReplaySubject(1);
  private readonly _horizotnalAngle$: ReplaySubject<number> = new ReplaySubject(1);
  private readonly _verticalAngle$: ReplaySubject<number> = new ReplaySubject(1);
  private readonly _fireControllerStatus$: ReplaySubject<string> = new ReplaySubject(1);
  private readonly _trackingEnabled$: ReplaySubject<boolean> = new ReplaySubject(1);

  public readonly cameraFps$: Observable<number>
  public readonly horizotnalAngle$: Observable<number>;
  public readonly verticalAngle$: Observable<number>;
  public readonly fireControllerStatus$: Observable<string>;
  public readonly trackingEnabled$: Observable<boolean>;

  constructor(private http: HttpClient) {
    this.cameraFps$ = this._cameraFps$.asObservable();
    this.horizotnalAngle$ = this._horizotnalAngle$.asObservable();
    this.verticalAngle$ = this._verticalAngle$.asObservable();
    this.fireControllerStatus$ = this._fireControllerStatus$.asObservable();
    this.trackingEnabled$ = this._trackingEnabled$.asObservable();

    setInterval(() => {
      firstValueFrom(this.http.get<StatusResult>('/api/status')).then((value) => {
        this._cameraFps$.next(value.cameraFps);
        this._fireControllerStatus$.next(value.fireControllerStatus);
        this._horizotnalAngle$.next(value.horizontalAngle);
        this._verticalAngle$.next(value.verticalAngle);
        this._trackingEnabled$.next(value.trackingEnabled);
      });
    }, 500)
  }

  public setHorizontalAngle(value: number): void {
    firstValueFrom(this.http.post<number>('/api/set_horizontal_angle', value)).then((value) => this._horizotnalAngle$.next(value));
  }

  public setVerticalAngle(value: number): void {
    firstValueFrom(this.http.post<number>('/api/set_vertical_angle', value)).then((value) => this._verticalAngle$.next(value));
  }

  public fire(): void {
    firstValueFrom(this.http.post<number>('/api/fire', {})).then(() => {});
  }

  public enableTracking(): void {
    firstValueFrom(this.http.post<number>('/api/enable_tracking', {})).then(() => {});
  }

  public disableTracking(): void {
    firstValueFrom(this.http.post<number>('/api/disable_tracking', {})).then(() => {});
  }
}
