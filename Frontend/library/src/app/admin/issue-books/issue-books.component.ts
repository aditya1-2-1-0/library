import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AdminService } from '../../services/admin.service';

@Component({
  selector: 'app-issue-book',
  templateUrl: './issue-books.component.html',
  styleUrls: ['./issue-books.component.css']
})
export class IssueBookComponent implements OnInit {
  issueBookForm!: FormGroup;

  constructor(private fb: FormBuilder, private adminService: AdminService) {}

  ngOnInit(): void {
    this.issueBookForm = this.fb.group({
      student: ['', Validators.required],
      book: ['', Validators.required],
      issue_date: ['', Validators.required],
      submission_date: ['', Validators.required],
      fine_per_day: ['', Validators.required]
    });
  }

  issueBook() {
    if (this.issueBookForm.valid) {
      const formData = this.issueBookForm.value;

      // The `student` and `book` fields are assumed to be IDs, but you may need to send more data if required
      const requestPayload = {
        student: formData.student,  // The ID of the student
        book: formData.book,        // The ID of the book
        issue_date: formData.issue_date,  // The issue date
        submission_date: formData.submission_date,  // The submission date
        fine_per_day: formData.fine_per_day  // Fine per day
      };

      this.adminService.issueBook(requestPayload).subscribe(response => {
        console.log('Book issued successfully', response);
      }, error => {
        console.log('Error:', error);
      });
    } else {
      console.log('Form is invalid');
    }
  }
}
