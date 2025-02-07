import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IssueBookComponent } from './issue-books.component';

describe('IssueBooksComponent', () => {
  let component: IssueBookComponent;
  let fixture: ComponentFixture<IssueBookComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [IssueBookComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IssueBookComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
