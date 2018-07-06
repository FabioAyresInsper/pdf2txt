import boto3
import os
import os.path
import subprocess

BUCKET_NAME = "justicaestadual"
S3_FOLDER = "diarios_03_04_2018"
TMP_DIR = "/tmp"
FILE_LIST = "filelist.txt"

def process_pdf_file(filename_pdf, bucket_name=BUCKET_NAME, s3_folder=S3_FOLDER, tmp_dir=TMP_DIR):
    filename_txt = filename_pdf[:-4] + ".txt"
    filename_log = filename_pdf[:-4] + ".log"

    pdf_key = s3_folder + "/" + filename_pdf
    txt_key = s3_folder + "/" + filename_txt
    log_key = s3_folder + "/" + filename_log

    path_pdf = os.path.join(tmp_dir, filename_pdf)
    path_txt = os.path.join(tmp_dir, filename_txt)
    path_log = os.path.join(tmp_dir, filename_log)

    # Download the pdf file.
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    bucket.download_file(pdf_key, path_pdf)

    # Convert to txt.
    result = subprocess.run(["java", "-jar", "pdfbox-app-2.0.11.jar", "ExtractText", "-debug",
                             path_pdf, path_txt], stderr=subprocess.PIPE)

    with open(path_log, "w") as f:
        f.write(result.stderr.decode("utf-8"))

    # Upload the txt and log files.
    bucket.upload_file(path_txt, txt_key)
    bucket.upload_file(path_log, log_key)

    # Delete the extra files.
    os.remove(path_pdf)
    os.remove(path_txt)
    os.remove(path_log)


if __name__ == "__main__":
    file_list = ["03042018MA.pdf"]
    for filename_pdf in file_list: 
        process_pdf_file(filename_pdf)

