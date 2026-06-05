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
git clone [https://github.com/YOUR_USERNAME/TabDataBuilder.git](https://github.com/charef00/TabDataBuilder.git)
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

### Install Poppler

The software uses `pdf2image`, which requires Poppler.

#### Windows

Download:

https://github.com/oschwartz10612/poppler-windows/releases

Extract Poppler and update:

```python
poppler_path=r"poppler-25.12.0\Library\bin"
```

inside `pdf.py`.

#### Linux

```bash
sudo apt install poppler-utils
```

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

## PaddleOCR API Configuration

Open:

```python
pdf.py
```

Locate:

```python
api_url = "YOUR_API_URL"
token = "YOUR_API_TOKEN"
```

Replace with your credentials:

```python
api_url = "https://xxxxx.aistudio-app.com/layout-parsing"
token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
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
