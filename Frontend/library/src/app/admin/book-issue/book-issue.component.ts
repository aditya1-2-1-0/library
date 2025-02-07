// import { Component, OnInit } from '@angular/core';
// import { FormBuilder, FormGroup, Validators } from '@angular/forms';
// import { BookService } from '../../services/book.service';
// import { StudentService } from '../../services/student.service';
// import { IssuedBookService } from '../../services/issued-book.service';

// @Component({
//   selector: 'app-book-issue',
//   templateUrl: './book-issue.component.html',
//   styleUrls: ['./book-issue.component.css']
// })
// export class BookIssueComponent implements OnInit {
//   issueBookForm: FormGroup;
//   books: any[] = [];
//   students: any[] = [];

//   constructor(
//     private fb: FormBuilder,
//     private bookService: BookService,
//     private studentService: StudentService,
//     private issuedBookService: IssuedBookService
//   ) {
//     this.issueBookForm = this.fb.group({
//       student: ['', Validators.required],
//       book: ['', Validators.required],
//       issue_date: ['', Validators.required],
//       submission_date: ['', Validators.required],
//       fine_per_day: ['', Validators.required]
//     });
//   }

//   ngOnInit(): void {
//     this.getBooks();
//     this.getStudents();
//   }

//   // Get all books from the backend
//   getBooks() {
//     this.bookService.getBooks().subscribe(
//       (response) => {
//         this.books = response;
//       },
//       (error) => {
//         console.log('Error fetching books:', error);
//       }
//     );
//   }

//   // Get all students from the backend
//   getStudents() {
//     this.studentService.getStudents().subscribe(
//       (response) => {
//         this.students = response;
//       },
//       (error) => {
//         console.log('Error fetching students:', error);
//       }
//     );
//   }

//   // Issue the book to the student
//   issueBook() {
//     if (this.issueBookForm.valid) {
//       this.issuedBookService.issueBook(this.issueBookForm.value).subscribe(
//         (response) => {
//           console.log('Book issued successfully:', response);
//           alert('Book issued successfully');
//         },
//         (error) => {
//           console.log('Failed to issue book:', error);
//           alert('Failed to issue book');
//         }
//       );
//     }
//   }
// }
