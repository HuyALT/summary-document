import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { summaryData } from '../models/summaryData';
import { datafile } from '../models/dataReadfile';



@Injectable({
  providedIn: 'root'
})
export class viSummarizeProcess{
    constructor(private http: HttpClient){}

    getSummary(datainput: string): Observable<summaryData>{
        const url  = "http://127.0.0.1:8080/api/summary"
        return this.http.post<summaryData>(url,{
            contents: datainput
        })
    }
    getFileDataText(formdata: FormData): Observable<datafile> {
        const url = "http://127.0.0.1:8080/api/getfiledata"
        return this.http.post<datafile>(url, formdata)
    }
}