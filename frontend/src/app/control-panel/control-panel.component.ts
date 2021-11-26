import { Component } from '@angular/core';
import { NerfBlasterService } from '../nerf-blaster.service';

@Component({
  selector: 'app-control-panel',
  templateUrl: './control-panel.component.html',
  styleUrls: ['./control-panel.component.scss']
})
export class ControlPanelComponent {
  constructor(private nerfBlasterService: NerfBlasterService) { }

  public fire(): void {
    this.nerfBlasterService.fire();
  }

  public onDraggedUp(): void {
    this.nerfBlasterService.setVerticalAngle(this.nerfBlasterService.verticalAngle + 5);
  }
  
  public onDraggedDown(): void {
    this.nerfBlasterService.setVerticalAngle(this.nerfBlasterService.verticalAngle - 5);
  }
  
  public onDraggedLeft(): void {    
    this.nerfBlasterService.setHorizontalAngle(this.nerfBlasterService.horizontalAngle - 5);
  }

  public onDraggedRight(): void {
    this.nerfBlasterService.setHorizontalAngle(this.nerfBlasterService.horizontalAngle + 5);
  }
}
