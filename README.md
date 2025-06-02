# FITS File Information Extractor

A user-friendly GUI tool for extracting metadata from astronomical FITS files. This tool helps astronomers and researchers easily extract key information from multiple FITS files and compile it into a well-organized CSV file.

## Features

- 📊 Extract essential FITS header information:
  - Right Ascension (RA)
  - Declination (DEC)
  - Exposure Time
  - Observation Date
- 🖱️ Simple point-and-click interface
- 📁 Process entire directories of FITS files
- 📈 Real-time progress tracking
- 📝 Detailed status updates
- 💾 Automatic CSV file generation with timestamps

## Installation

### On Linux/Mac:
1. Clone this repository:
   ```bash
   git clone https://github.com/dipang8867/fits-info-extractor.git
   cd fits-info-extractor
   ```

2. Run the installation script:
   ```bash
   ./install.sh
   ```

### On Windows:
1. Clone this repository:
   ```bash
   git clone https://github.com/dipang8867/fits-info-extractor.git
   cd fits-info-extractor
   ```

2. Double-click on `install.bat`
   
   OR run from command prompt:
   ```batch
   install.bat
   ```

The installation script will:
- Create a Python virtual environment
- Install all required dependencies
- Set up everything needed to run the program

## Usage

1. Run the application:
   ```bash
   python fits_gui.py
   ```

2. Click "Select Directory" to choose the folder containing your FITS files
3. Click "Extract Information" to begin processing
4. Monitor progress in the status window
5. When complete, find your CSV file in the same directory

## Output Format

The generated CSV file includes the following columns:
- `File`: Name of the FITS file
- `Path`: Full path to the file
- `RA`: Right Ascension (degrees)
- `DEC`: Declination (degrees)
- `Exposure_Time`: Exposure time in seconds
- `Date_Obs`: Date of observation

## Supported FITS Keywords

The tool looks for the following FITS header keywords:
- RA/CRVAL1 (Right Ascension)
- DEC/CRVAL2 (Declination)
- EXPTIME/EXPOSURE (Exposure Time)
- DATE-OBS/DATE (Observation Date)

## Error Handling

- The tool continues processing even if some files have errors
- All errors are displayed in the status window
- Files with missing keywords will show "N/A" in the corresponding fields
- The tool handles both compressed and uncompressed FITS files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Uses [Astropy](https://www.astropy.org/) for FITS file handling
- Inspired by the needs of the astronomical community
