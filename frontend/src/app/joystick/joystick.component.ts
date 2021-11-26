import { Component, ElementRef, AfterViewInit, ViewChild, OnDestroy, Output, EventEmitter } from '@angular/core';
import { create, Joystick, JoystickManagerOptions, Position } from 'nipplejs';

@Component({
  selector: 'app-joystick',
  templateUrl: './joystick.component.html',
  styleUrls: ['./joystick.component.scss']
})
export class JoystickComponent implements AfterViewInit, OnDestroy {
  @ViewChild('joystickContainer')
  public joystickContainer: ElementRef<HTMLInputElement> | null = null;
  
  @Output() public onDraggedUp = new EventEmitter<void>();
  @Output() public onDraggedDown = new EventEmitter<void>();
  @Output() public onDraggedLeft = new EventEmitter<void>();
  @Output() public onDraggedRight = new EventEmitter<void>();

  private intervalId: any = null;

  public ngAfterViewInit(): void {
    const joystickManagerOptions: JoystickManagerOptions = {
      zone: this.joystickContainer?.nativeElement,
      mode: 'static',
      position: {left: '50%', top: '50%'},
      color: 'red'
    }

    const manager = create(joystickManagerOptions);
    const joystick: Joystick = manager.get(0);
    joystick.on('start', () => {
      this.intervalId = setInterval(() => {
        const position = joystick.frontPosition;
        if (position) this.handleDrag(position);
      }, 100);
    })

    joystick.on('end', () => {
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
      this.onDraggedRight.emit();
    } else if (position.x < threshold * -1) {
      this.onDraggedLeft.emit();
    }

    if (position.y > threshold) {
      this.onDraggedUp.emit();
    } else if (position.y < threshold * -1) {
      this.onDraggedDown.emit();
    }
  }
}
