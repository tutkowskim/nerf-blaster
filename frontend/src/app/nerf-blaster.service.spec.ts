import { TestBed } from '@angular/core/testing';

import { NerfBlasterService } from './nerf-blaster.service';

describe('NerfBlasterService', () => {
  let service: NerfBlasterService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NerfBlasterService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
