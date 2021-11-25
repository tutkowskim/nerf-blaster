import { Component, OnInit } from '@angular/core';
import { NerfBlasterService } from '../nerf-blaster.service';

@Component({
  selector: 'app-control-panel',
  templateUrl: './control-panel.component.html',
  styleUrls: ['./control-panel.component.scss']
})
export class ControlPanelComponent implements OnInit {
  constructor(private nerfBlasterService: NerfBlasterService) { }

  ngOnInit(): void {
  }

  public fire(): void {
    this.nerfBlasterService.fire();
  }
}
