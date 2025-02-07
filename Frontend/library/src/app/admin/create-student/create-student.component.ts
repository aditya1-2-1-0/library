import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AdminService } from '../../services/admin.service';

@Component({
  selector: 'app-create-student',
  templateUrl: './create-student.component.html',
  styleUrls: ['./create-student.component.css']
})
export class CreateStudentComponent implements OnInit {
  studentForm!: FormGroup;

  constructor(private fb: FormBuilder, private adminService: AdminService) {}

  ngOnInit(): void {
    this.studentForm = this.fb.group({
      name: ['', Validators.required],
      class_name: ['', Validators.required],
      roll_no: ['', Validators.required],
      phone_number: ['', Validators.required],
      user: this.fb.group({
        email: ['', [Validators.required, Validators.email]],
        password: ['', Validators.required],
      }),
    });
  }
  
  createStudent() {
    if (this.studentForm.valid) {
      this.adminService.createStudent(this.studentForm.value).subscribe(
        (response) => {
          console.log('Student created successfully', response);
          alert('Student created successfully!');
          this.studentForm.reset();
        },
        (error) => {
          console.log('Error:', error);
          alert('An error occurred while creating the student. Please try again.');
        }
      );
    }
  }
}