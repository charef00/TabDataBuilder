
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    send_from_directory,
    send_file,
    abort
)

from pdf import *
import os
import json
import secrets
import pandas as pd
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# =====================================================
# PATHS
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PAPERS_DIR = os.path.join(
    BASE_DIR,
    "papers"
)

TABLES_DIR = os.path.join(
    BASE_DIR,
    "tables"
)

EXCEL_DIR = os.path.join(
    BASE_DIR,
    "excel"
)

DATASET_FILE = os.path.join(
    BASE_DIR,
    "dataset.json"
)

for folder in [
    PAPERS_DIR,
    TABLES_DIR,
    EXCEL_DIR
]:
    os.makedirs(
        folder,
        exist_ok=True
    )

if not os.path.exists(
    DATASET_FILE
):

    with open(
        DATASET_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "columns": [],
                "rows": []
            },
            f
        )




# =====================================================
# HOME
# =====================================================

@app.route("/")
def index():
    clear_all()
    return render_template(
        "index.html"
    )


# =====================================================
# UPLOAD PDF
# =====================================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload_files():

    if "files[]" not in request.files:
        return jsonify({
            "status":"error",
            "message":
                "No files selected"
        })

    files = request.files.getlist(
        "files[]"
    )

    uploaded = []

    for file in files:

        if (
            file and
            file.filename.lower()
            .endswith(".pdf")
        ):

            filename = secure_filename(
                file.filename
            )

            save_path = os.path.join(
                PAPERS_DIR,
                filename
            )

            file.save(save_path)

            uploaded.append(
                filename
            )

    return redirect(
        url_for(
            "start_processing"
        )
    )


# =====================================================
# START PROCESSING
# =====================================================

@app.route(
    "/start_processing"
)
def start_processing():

    pdf_files = [

        f for f in
        os.listdir(PAPERS_DIR)

        if f.lower()
        .endswith(".pdf")
    ]

    if not pdf_files:

        return render_template(
            "index.html",
            error=
            "No PDF uploaded"
        )

    session["pdf_files"] = (
        pdf_files
    )

    session["total_pdfs"] = (
        len(pdf_files)
    )

    session["current_index"] = 0

    return redirect(
        url_for(
            "processing"
        )
    )


# =====================================================
# PROCESS PDF
# =====================================================

@app.route("/processing")
def processing():

    if (
        "pdf_files"
        not in session
    ):
        return redirect(
            url_for("index")
        )

    pdf_files = session[
        "pdf_files"
    ]

    total = session[
        "total_pdfs"
    ]

    current_index = session.get(
        "current_index",
        0
    )

    # FINISHED
    if current_index >= total:

        images = os.listdir(
            TABLES_DIR
        )

        return render_template(
            "tables_select.html",
            total=total,
            images=images
        )

    current_pdf = pdf_files[
        current_index
    ]

    file_path = os.path.join(
        PAPERS_DIR,
        current_pdf
    )

    try:

        if os.path.isfile(
            file_path
        ):

            pdf_to_tables_png(
                pdf_path=file_path
            )

    except Exception as e:

        print(
            f"ERROR: {e}"
        )

    return render_template(
        "processing.html",
        current_doi=current_pdf,
        progress=
            current_index + 1,
        total=total,
        title=current_pdf,
        current_index=
            current_index
    )





# =====================================================
# NEXT PDF
# =====================================================

@app.route(
    "/process_next",
    methods=["POST"]
)
def process_next():

    current_index = session.get(
        "current_index",
        0
    )

    current_index += 1

    session[
        "current_index"
    ] = current_index

    if (
        current_index <
        len(
            session[
                "pdf_files"
            ]
        )
    ):

        return jsonify({
            "next": True
        })

    return jsonify({
        "complete": True
    })


# =====================================================
# SHOW TABLE IMAGE
# =====================================================

@app.route(
    "/tables/<path:filename>"
)
def tables(filename):

    file_path = os.path.join(
        TABLES_DIR,
        filename
    )

    if not os.path.exists(
        file_path
    ):
        abort(404)

    return send_from_directory(
        TABLES_DIR,
        filename
    )


# =====================================================
# SELECT TABLES
# =====================================================

@app.route(
    "/process-tables",
    methods=["POST"]
)
def process_tables():

    selected_tables = (
        request.form.getlist(
            "selected_images"
        )
    )

    session[
        "tables_queue"
    ] = selected_tables

    session[
        "tables_total"
    ] = len(
        selected_tables
    )

    return redirect(
        url_for(
            "process_next_table"
        )
    )


# =====================================================
# OCR PAGE
# =====================================================

@app.route(
    "/process-next-table"
)
def process_next_table():

    tables_queue = session.get(
        "tables_queue",
        []
    )

    total = session.get(
        "tables_total",
        0
    )

    if not tables_queue:

        session["mapper_files"] = [

            f for f in
            os.listdir(EXCEL_DIR)

            if f.endswith(".xlsx")
        ]

        session["mapper_index"] = 0

        return redirect(
            url_for(
                "mapper_view"
            )
        )

    current_image = (
        tables_queue[0]
    )

    processed = (
        total -
        len(
            tables_queue
        )
    )

    progress = int(
        (
            processed
            / total
        ) * 100
    ) if total else 100

    return render_template(
        "progress.html",
        current_image=
            current_image,
        progress=
            progress,
        processed=
            processed,
        total=total
    )


# =====================================================
# OCR
# =====================================================

@app.route("/run-ocr")
def run_ocr():

    tables_queue = session.get(
        "tables_queue",
        []
    )

    if not tables_queue:
        return redirect(
            url_for(
                "process_next_table"
            )
        )

    current_image = (
        tables_queue.pop(0)
    )

    table_html = (
        extract_table_html(
            f"tables/"
            f"{current_image}"
        )
    )

    new_name = (
        current_image
        .rsplit(".",1)[0]
        + ".xlsx"
    )

    output_path = os.path.join(
        EXCEL_DIR,
        new_name
    )
    
    DATASET_FILE = os.path.join(
        BASE_DIR,
        "dataset.json"
    )

    html_table_to_excel(
        html_table=
            table_html,
        output_path=
            output_path
    )

    session[
        "tables_queue"
    ] = tables_queue

    return redirect(
        url_for(
            "process_next_table"
        )
    )


# =====================================================
# TABLE MAPPER
# =====================================================

@app.route("/table-mapper")
def table_mapper():

    excel_files = [

        f for f in
        os.listdir(EXCEL_DIR)

        if f.endswith(
            ".xlsx"
        )

        and
        f != "final.xlsx"
    ]

    session[
        "mapper_files"
    ] = excel_files

    if (
        "mapper_index"
        not in session
    ):
        session[
            "mapper_index"
        ] = 0

    return redirect(
        url_for(
            "mapper_view"
        )
    )


@app.route("/mapper-view")
def mapper_view():

    files = session.get(
        "mapper_files",
        []
    )

    if not files:

        return redirect(
            url_for("index")
        )

    index = session.get(
        "mapper_index",
        0
    )

    if index >= len(files):
        index = len(files)-1

    current_file = files[index]

    path = os.path.join(
        EXCEL_DIR,
        current_file
    )

    df = pd.read_excel(
        path,
        header=None
    )

    table_data = (
        df.fillna("NaN")
        .astype(str)
        .values.tolist()
    )

    return render_template(
        "table_mapper.html",
        table_data=table_data,
        file_name=current_file,
        current=index+1,
        total=len(files)
    )





# =====================================================
# NEXT
# =====================================================


@app.route("/mapper-next")
def mapper_next():

    files = session.get(
        "mapper_files",
        []
    )

    index = session.get(
        "mapper_index",
        0
    )

    if index < len(files)-1:

        session[
            "mapper_index"
        ] = index + 1

    return redirect(
        url_for(
            "mapper_view"
        )
    )



@app.route("/mapper-prev")
def mapper_prev():

    index = session.get(
        "mapper_index",
        0
    )

    if index > 0:

        session[
            "mapper_index"
        ] = index - 1

    return redirect(
        url_for(
            "mapper_view"
        )
    )





# =====================================================
# DATASET
# =====================================================

@app.route("/load-dataset")
def load_dataset():

    if not os.path.exists(
        DATASET_FILE
    ):

        return jsonify({
            "columns": [],
            "rows": []
        })

    with open(
        DATASET_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        dataset = json.load(
            f
        )

    return jsonify(
        dataset
    )


@app.route(
    "/save-dataset",
    methods=["POST"]
)
def save_dataset():

    data = request.json

    with open(
        DATASET_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    return jsonify({
        "status": "saved"
    })



@app.route("/export-dataset")
def export_dataset():

    if not os.path.exists(
        DATASET_FILE
    ):
        return "Dataset not found"

    with open(
        DATASET_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        columns_data = json.load(f)

    if not columns_data:
        return "Dataset empty"

    data = {}

    max_length = 0

    for column in columns_data:

        label = column["label"]

        values = column["values"]

        data[label] = values

        max_length = max(
            max_length,
            len(values)
        )

    for label in data:

        while (
            len(data[label])
            < max_length
        ):
            data[label].append("")

    df = pd.DataFrame(
        data
    )

    output_file = os.path.join(
        EXCEL_DIR,
        "final.xlsx"
    )

    df.to_excel(
        output_file,
        index=False
    )

    return send_file(
        output_file,
        as_attachment=True
    )


# =====================================================
# CLEAR
# =====================================================

@app.route(
    "/clear-all",
    methods=["POST"]
)
def clear_all():

    folders = [

        PAPERS_DIR,
        TABLES_DIR,
        EXCEL_DIR
    ]
    if os.path.exists(
        DATASET_FILE
    ):
        os.remove(
            DATASET_FILE
        )

    if os.path.exists(
        DATASET_FILE
    ):
        os.remove(
            DATASET_FILE
        )

    with open(
        DATASET_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "columns": [],
                "rows": []
            },
            f
        )

    for folder in folders:

        for file in os.listdir(
            folder
        ):

            path = os.path.join(
                folder,
                file
            )

            if os.path.isfile(
                path
            ):
                os.remove(path)
        

    return jsonify({
        "status":
            "success"
    })


if __name__ == "__main__":
    app.run(
        debug=True
    )
