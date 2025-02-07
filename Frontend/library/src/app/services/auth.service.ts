// import { Injectable } from '@angular/core';
// import { HttpClient, HttpHeaders } from '@angular/common/http';
// import { Observable, throwError } from 'rxjs';

// @Injectable({
//   providedIn: 'root'
// })
// export class AuthService {
//   isAuthenticated() {
//     throw new Error('Method not implemented.');
//   }
//   private baseUrl = 'http://127.0.0.1:8000/api/';

//   constructor(private http: HttpClient) {}

//   login(data: any): Observable<any> {
//     return this.http.post(`${this.baseUrl}login/`, data);
//   }

//   register(data: any): Observable<any> {
//     return this.http.post(`${this.baseUrl}students/create/`, data);
//   }

//   verifyOTP(data: any): Observable<any> {
//     return this.http.post(`${this.baseUrl}otp-verify/`, data);
//   }

  
//   getIssuedBook(authHeaders: HttpHeaders): Observable<any> {
//     const token = localStorage.getItem('token');
    
//     if (!token) {
//       return throwError('No token found');  // Or handle token error
//     }
  
//     // Only add the Authorization header if it's not present in authHeaders
//     let headers = authHeaders;
//     if (!headers.has('Authorization')) {
//       headers = headers.set('Authorization', `Bearer ${token}`);
//     }
  
//     return this.http.get<any>(`${this.baseUrl}student/issued_books/`, { headers });
//   }
  

//   resetPassword(uid: string, token: string, password: string): Observable<any> {
//     const url = `${this.baseUrl}reset-password/`;  // Update the endpoint if necessary
//     const body = { uid, token, password };
//     return this.http.post<any>(url, body);
//   }

// }
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private baseUrl = 'http://127.0.0.1:8000/api/';

  constructor(private http: HttpClient) {}

  // Method to check if the user is authenticated
  isAuthenticated(): boolean {
    // Check if the token exists in localStorage
    const token = localStorage.getItem('token');
    return !!token; // Returns true if token exists, otherwise false
  }

  // Login method
  login(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}login/`, data);
  }

  // Register method for creating students
  register(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}students/create/`, data);
  }

  // OTP Verification method
  verifyOTP(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}otp-verify/`, data);
  }

  // Fetch issued books with the Authorization header
  getIssuedBook(authHeaders: HttpHeaders): Observable<any> {
    const token = localStorage.getItem('token');
    if (!token) {
      return throwError('No token found');
    }

    let headers = authHeaders;
    if (!headers.has('Authorization')) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }

    return this.http.get<any>(`${this.baseUrl}student/issued_books/`, { headers });
  }

  // Reset password API
  resetPassword(uid: string, token: string, password: string): Observable<any> {
    const url = `${this.baseUrl}reset-password/`;
    const body = { uid, token, password };
    return this.http.post<any>(url, body);
  }
}
