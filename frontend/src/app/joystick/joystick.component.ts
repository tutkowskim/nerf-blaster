import { Component, ElementRef, AfterViewInit, ViewChild, OnDestroy } from '@angular/core';
import { create, Joystick, JoystickManagerOptions, Position } from 'nipplejs';
import { NerfBlasterService } from '../nerf-blaster.service';

@Component({
  selector: 'app-joystick',
  templateUrl: './joystick.component.html',
  styleUrls: ['./joystick.component.scss']
})
export class JoystickComponent implements AfterViewInit, OnDestroy {
  @ViewChild('joystickContainer')
  public joystickContainer: ElementRef<HTMLInputElement> | null = null;
  private intervalId: any = null;

  constructor(private nerfBlasterService: NerfBlasterService) {}

  public ngAfterViewInit(): void {
    const joystickManagerOptions: JoystickManagerOptions = {
      zone: this.joystickContainer?.nativeElement,
      mode: 'static',
      position: {left: '50%', top: '50%'},
      color: 'red'
    }

    const manager = create(joystickManagerOptions);
    manager.on('start', (_evt, data) => {
      this.intervalId = setInterval(() => {
        const position = manager.get(data.identifier)?.frontPosition;
        if (position) this.handleDrag(position);
      }, 100);
    })

    manager.on('end', () => {
      if (this.intervalId) {
        clearInterval(this.intervalId)
        this.intervalId = null;
      }
    })
  }

  public ngOnDestroy(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId)
    }
  }

  public handleDrag(position: Position): void {
    const threshold = 20;
    if (position.x > threshold) {
      this.nerfBlasterService.setHorizontalAngle(this.nerfBlasterService.horizontalAngle + 5);
    } else if (position.x < threshold * -1) {
      this.nerfBlasterService.setHorizontalAngle(this.nerfBlasterService.horizontalAngle - 5);
    }

    if (position.y > threshold) {
      this.nerfBlasterService.setVerticalAngle(this.nerfBlasterService.verticalAngle + 5);
    } else if (position.y < threshold * -1) {
      this.nerfBlasterService.setVerticalAngle(this.nerfBlasterService.verticalAngle - 5);
    }
  }
}
