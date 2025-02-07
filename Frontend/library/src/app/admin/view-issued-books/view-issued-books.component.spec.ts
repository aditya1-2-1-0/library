import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewIssuedBooksComponent } from './view-issued-books.component';

describe('ViewIssuedBooksComponent', () => {
  let component: ViewIssuedBooksComponent;
  let fixture: ComponentFixture<ViewIssuedBooksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ViewIssuedBooksComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewIssuedBooksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
