import { Component, OnInit } from '@angular/core';
import { AdminService } from '../../services/admin.service';

@Component({
  selector: 'app-view-issued-books',
  templateUrl: './view-issued-books.component.html',
  styleUrls: ['./view-issued-books.component.css']
})
export class ViewIssuedBooksComponent implements OnInit {
  issuedBooks: any[] = [];

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.adminService.getIssuedBooks().subscribe(response => {
      this.issuedBooks = response;
    }, error => {
      console.log('Error:', error);
    });
  }
}
