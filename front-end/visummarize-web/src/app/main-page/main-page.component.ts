import { Component, OnInit } from '@angular/core';
import { viSummarizeProcess } from '../callapi/visummarize';
import { summaryData } from '../models/summaryData';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrl: './main-page.component.css'
})
export class MainPageComponent implements OnInit {
  textInput: string = ""
  textOutput: string = ""
  fileSelected!: File
  resultSummary: summaryData = {
    message: "",
    summaryData: ""
  }

  constructor(private summary: viSummarizeProcess){}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const selectedFile = input.files[0];

      const formData = new FormData();
      formData.append('file', selectedFile, selectedFile.name);

      this.summary.getFileDataText(formData).subscribe({
        next: data=>{
          this.textInput = data.data
        }
      })
      
    }
  }

  ngOnInit(): void {
    
  }
  startsumary(){
    this.summary.getSummary(this.textInput).subscribe({
      next: data=>{
        this.resultSummary = data
        this.textOutput = data.summaryData
      }
    })
  }
  
}
