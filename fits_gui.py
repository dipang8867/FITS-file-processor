#!/usr/bin/env python3

import os
import sys
from astropy.io import fits
import pandas as pd
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                           QHBoxLayout, QWidget, QFileDialog, QLabel, QProgressBar,
                           QTextEdit, QLineEdit)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

class FitsExtractorWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(list)
    
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        
    def run(self):
        fits_data = []
        total_files = sum(1 for _, _, files in os.walk(self.directory) 
                         for f in files if f.lower().endswith(('.fits', '.fit', '.fts')))
        processed = 0
        
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.lower().endswith(('.fits', '.fit', '.fts')):
                    file_path = os.path.join(root, file)
                    try:
                        with fits.open(file_path) as hdul:
                            header = hdul[0].header
                            
                            info = {
                                'File': file,
                                'Path': file_path,
                                'RA': header.get('RA', 'N/A'),
                                'DEC': header.get('DEC', 'N/A'),
                                'Exposure_Time': header.get('EXPTIME', 'N/A'),
                                'Date_Obs': header.get('DATE-OBS', header.get('DATE', 'N/A')),
                            }
                            
                            if info['RA'] == 'N/A':
                                info['RA'] = header.get('CRVAL1', 'N/A')
                            if info['DEC'] == 'N/A':
                                info['DEC'] = header.get('CRVAL2', 'N/A')
                            if info['Exposure_Time'] == 'N/A':
                                info['Exposure_Time'] = header.get('EXPOSURE', 'N/A')
                            
                            fits_data.append(info)
                            
                    except Exception as e:
                        self.status.emit(f"Error processing {file}: {str(e)}")
                    
                    processed += 1
                    progress = int((processed / total_files) * 100)
                    self.progress.emit(progress)
                    
        self.finished.emit(fits_data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FITS File Information Extractor")
        self.setMinimumSize(800, 600)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create header
        header = QLabel("FITS File Information Extractor")
        header.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Create description
        description = QLabel(
            "This tool extracts RA, Dec, Exposure time, and observation date "
            "from FITS files in a directory and saves the information to a CSV file."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)
        
        # Create directory selection
        dir_group = QWidget()
        dir_layout = QHBoxLayout(dir_group)
        
        dir_label = QLabel("FITS Directory:")
        dir_label.setMinimumWidth(100)
        dir_layout.addWidget(dir_label)
        
        self.dir_path = QLineEdit()
        self.dir_path.setReadOnly(True)
        self.dir_path.setPlaceholderText("Select directory containing FITS files...")
        dir_layout.addWidget(self.dir_path)
        
        select_btn = QPushButton("Browse...")
        select_btn.clicked.connect(self.select_directory)
        dir_layout.addWidget(select_btn)
        
        layout.addWidget(dir_group)
        
        # Create output file name selection
        output_group = QWidget()
        output_layout = QHBoxLayout(output_group)
        
        output_label = QLabel("Output CSV:")
        output_label.setMinimumWidth(100)
        output_layout.addWidget(output_label)
        
        self.output_name = QLineEdit()
        self.output_name.setPlaceholderText("Enter output CSV filename...")
        self.output_name.setText("fits_info.csv")
        output_layout.addWidget(self.output_name)
        
        layout.addWidget(output_group)
        
        # Create progress bar
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # Create status text area
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMinimumHeight(200)
        layout.addWidget(self.status_text)
        
        # Create extract button
        self.extract_btn = QPushButton("Extract Information")
        self.extract_btn.clicked.connect(self.start_extraction)
        self.extract_btn.setEnabled(False)
        layout.addWidget(self.extract_btn)
        
        self.directory = None
        self.worker = None
        
    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", "",
            QFileDialog.Option.ShowDirsOnly
        )
        if directory:
            self.directory = directory
            self.dir_path.setText(directory)
            self.extract_btn.setEnabled(True)
            self.status_text.clear()
            
    def start_extraction(self):
        if not self.directory:
            self.update_status("Please select a directory first!")
            return
            
        output_name = self.output_name.text().strip()
        if not output_name:
            self.update_status("Please enter an output filename!")
            return
        
        if not output_name.endswith('.csv'):
            output_name += '.csv'
            
        self.extract_btn.setEnabled(False)
        self.progress.setValue(0)
        self.status_text.clear()
        
        self.worker = FitsExtractorWorker(self.directory)
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(lambda data: self.save_results(data, output_name))
        self.worker.start()
        
    def update_progress(self, value):
        self.progress.setValue(value)
        
    def update_status(self, message):
        self.status_text.append(message)
        
    def save_results(self, data, output_name):
        if not data:
            self.update_status("No FITS files found!")
            self.extract_btn.setEnabled(True)
            return
        
        # Save the CSV file in the selected directory
        output_path = os.path.join(self.directory, output_name)
        
        try:
            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False)
            self.update_status(f"\nInformation saved to {output_path}")
        except Exception as e:
            self.update_status(f"\nError saving file: {str(e)}")
        
        self.extract_btn.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
