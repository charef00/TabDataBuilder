# TabDataBuilder
TabDataBuilder is a web-based platform for automated table extraction and interactive dataset construction from PDF documents. The software combines YOLO-based table detection, PaddleOCR-based content extraction, and a human-in-the-loop validation interface to transform tabular information from scientific publications into structured datasets.

## Overview

TabDataBuilder automates the extraction of tabular data from PDF documents by combining YOLO-based table detection, PaddleOCR-based content extraction, and a human-in-the-loop validation interface. The platform enables researchers to transform tables embedded in scientific publications into structured and reusable datasets suitable for statistical analysis, systematic reviews, meta-analyses, and machine learning applications.

## Features

* Upload one or multiple PDF documents.
* Automatic PDF-to-image conversion.
* YOLO-based table detection.
* Automatic table extraction and cropping.
* PaddleOCR-based table reconstruction.
* Interactive table selection.
* Human-in-the-loop dataset construction.
* Column creation, modification, and deletion.
* Value editing and validation.
* Export final datasets to Excel format.

## Installation

### Clone Repository

```bash
git clone https://github.com/charef00/TabDataBuilder.git
cd TabDataBuilder
```

### Create Environment

#### Conda

```bash
conda create -n tabdatabuilder python=3.11 -y
conda activate tabdatabuilder
```

#### Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Additional Requirements

## Install Poppler

TabDataBuilder uses **pdf2image** to convert PDF pages into images. Therefore, **Poppler** must be installed before running the application.

### Windows

1. Download Poppler from:

   https://github.com/oschwartz10612/poppler-windows/releases

2. Extract the downloaded archive.

3. Locate the Poppler binary directory:

```text
poppler-25.12.0/
└── Library/
    └── bin/
```

4. Update the `poppler_path` parameter in `pdf.py`:

```python
poppler_path=r"poppler-25.12.0\Library\bin"
```

Alternatively, use the full absolute path:

```python
poppler_path=r"C:\poppler\Library\bin"
```

### Linux (Ubuntu/Debian)

Install Poppler using:

```bash
sudo apt update
sudo apt install poppler-utils
```

Verify installation:

```bash
pdfinfo -v
```

### macOS

Install Poppler using Homebrew:

```bash
brew install poppler
```

Verify installation:

```bash
pdfinfo -v
```

### Verify Installation

After installation, run:

```bash
pdfinfo -v
```

If Poppler is correctly installed, the command should display the installed version instead of returning an error.

If the application reports:

```text
Unable to get page count. Is poppler installed and in PATH?
```

verify that Poppler is installed correctly and that the `poppler_path` specified in `pdf.py` points to the correct `bin` directory.


## YOLO Model

Download the DocLayNet model:

Direct download:

https://huggingface.co/hantian/yolo-doclaynet/resolve/main/yolov8x-doclaynet.pt

Project page:

https://huggingface.co/hantian/yolo-doclaynet/blob/main/yolov8x-doclaynet.pt

Place the model in the project root:

```text
TabDataBuilder/
│
├── yolov8x-doclaynet.pt
```

or modify:

```python
model_path="yolov8x-doclaynet.pt"
```

inside `pdf.py`.


```

## Running the Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Usage Workflow

### Step 1 – Upload PDF Documents

Upload one or multiple scientific articles in PDF format.

### Step 2 – Table Detection

PDF pages are converted into images and processed using the YOLO DocLayNet model to detect tables.

### Step 3 – Table Selection

Review detected tables and select the relevant ones for extraction.

### Step 4 – OCR Extraction

Selected tables are processed using PaddleOCR and converted into HTML tables.

### Step 5 – Dataset Construction

Create custom columns and build a dataset by selecting values directly from OCR-generated tables.

Available operations:

* Create columns.
* Rename columns.
* Delete columns.
* Add values.
* Edit values.
* Delete values.
* Navigate between extracted tables.
* Validate extracted data.

### Step 6 – Export Dataset

Export the final dataset as an Excel file (`.xlsx`).

## Project Structure

```text
TabDataBuilder/
│
├── app.py
├── pdf.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── templates/
├── static/
│
├── papers/
├── tables/
├── excel/
│
├── dataset.json
│
└── yolov8x-doclaynet.pt
```

## Demonstration Video

Video tutorial:

```text
https://YOUR_VIDEO_LINK
```

## Citation

```bibtex
@article{charef2026tabdatabuilder,
  title={TabDataBuilder: A Web-Based Software for Automated Table Extraction and Interactive Dataset Construction from PDF Documents},
  author={Charef, Ayoub},
  journal={SoftwareX},
  year={2026}
}
```

## License

This project is released under the MIT License.

```text
MIT License

Copyright (c) 2026 Ayoub Charef

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.
```

## Author

**Ayoub Charef**

* Artificial Intelligence Researcher
* Computer Science Professor
* Software Developer

Contributions, suggestions, and pull requests are welcome.
