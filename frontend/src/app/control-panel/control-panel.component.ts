import { Component } from '@angular/core';
import { firstValueFrom, Observable } from 'rxjs';
import { NerfBlasterService } from '../nerf-blaster.service';

@Component({
  selector: 'app-control-panel',
  templateUrl: './control-panel.component.html',
  styleUrls: ['./control-panel.component.scss']
})
export class ControlPanelComponent {
  public readonly status$: Observable<string>;
  public readonly trackingEnabled$: Observable<boolean>;

  constructor(private nerfBlasterService: NerfBlasterService) {
    this.status$ = this.nerfBlasterService.fireControllerStatus$;
    this.trackingEnabled$ = this.nerfBlasterService.trackingEnabled$;
  }

  public fire(): void {
    this.nerfBlasterService.fire();
  }

  public onDraggedUp(): void {
    firstValueFrom(this.nerfBlasterService.verticalAngle$).then((angle) => {
      this.nerfBlasterService.setVerticalAngle(angle + 5);
    });    
  }
  
  public onDraggedDown(): void {
    firstValueFrom(this.nerfBlasterService.verticalAngle$).then((angle) => {
      this.nerfBlasterService.setVerticalAngle(angle - 5);
    });
  }
  
  public onDraggedLeft(): void {
    firstValueFrom(this.nerfBlasterService.horizotnalAngle$).then((angle) => {
      this.nerfBlasterService.setHorizontalAngle(angle - 5);
    });  
  }

  public onDraggedRight(): void {
    firstValueFrom(this.nerfBlasterService.horizotnalAngle$).then((angle) => {
      this.nerfBlasterService.setHorizontalAngle(angle + 5);
    });
  }

  public enableTracking(): void {
    this.nerfBlasterService.enableTracking();
  }

  public disableTracking(): void {
    this.nerfBlasterService.disableTracking();
  }
}
