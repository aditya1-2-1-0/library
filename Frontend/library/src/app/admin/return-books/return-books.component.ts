import { Component } from '@angular/core';
import { AdminService } from '../../services/admin.service';

@Component({
  selector: 'app-return-book', 
  templateUrl: './return-books.component.html',
  styleUrls: ['./return-books.component.css']
})
export class ReturnBookComponent {
  bookId: number = 0;;

  constructor(private adminService: AdminService) {}

  returnBook() {
    if (this.bookId) {
      this.adminService.returnBook(this.bookId).subscribe(response => {
        console.log('Book returned successfully', response);
      }, error => {
        console.log('Error:', error);
      });
    }
  }
}
