import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AdminService } from '../../services/admin.service';
import { MatSnackBar } from '@angular/material/snack-bar';  // Import MatSnackBar for alerts

@Component({
  selector: 'app-create-book',
  templateUrl: './create-books.component.html',
  styleUrls: ['./create-books.component.css']
})
export class CreateBookComponent implements OnInit {
  bookForm!: FormGroup;

  constructor(
    private fb: FormBuilder, 
    private adminService: AdminService,
    private snackBar: MatSnackBar  
  ) {}

  ngOnInit(): void {
    this.bookForm = this.fb.group({
      name: ['', Validators.required],
      author: ['', Validators.required],
      subject: ['', Validators.required],
      description: ['', Validators.required],
      price: ['', Validators.required]
    });
  }

  createBook() {
    if (this.bookForm.valid) {
      this.adminService.createBook(this.bookForm.value).subscribe(
        response => {
          this.snackBar.open('Book created successfully!', 'Close', {
            duration: 3000, 
            verticalPosition: 'top',
            horizontalPosition: 'center',
            panelClass: ['snack-bar-success'] 
          });

          this.bookForm.reset();
        },
        error => {
          this.snackBar.open('Error creating book. Please try again.', 'Close', {
            duration: 3000,
            verticalPosition: 'top',
            horizontalPosition: 'center',
            panelClass: ['snack-bar-error'] 
          });

          console.log('Error:', error);
        }
      );
    }
  }
}
