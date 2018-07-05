import boto3
import os.path
import subprocess

BUCKET_NAME = "justicaestadual"
S3_FOLDER = "diarios_03_04_2018"
DIR_PDF = "./data"
DIR_TXT = "./txt"
DIR_LOG = "./log"

def download_pdf(filename_pdf, bucket_name=BUCKET_NAME, s3_folder=S3_FOLDER, 
                 dir_pdf=DIR_PDF):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    key = s3_folder + "/" + filename_pdf
    bucket.download_file(key, os.path.join(dir_pdf, filename_pdf))

def upload_txt(filename_pdf, bucket_name=BUCKET_NAME, s3_folder=S3_FOLDER, 
               dir_txt=DIR_TXT):
    pass

def convert_pdf_to_txt(filename_pdf, dir_pdf=DIR_PDF, dir_txt=DIR_TXT, 
                       dir_log=DIR_LOG):
    filename_txt = filename_pdf[:-4] + ".txt"
    result = subprocess.run([
        "java", "-jar", "pdfbox-app-2.0.11.jar", "ExtractText", "-debug", 
        os.path.join(dir_pdf, filename_pdf),
        os.path.join(dir_txt, filename_txt)], 
        stderr=subprocess.PIPE)

    filename_log = filename_pdf[:-4] + ".log"
    with open(os.path.join(dir_log, filename_log), "w") as f:
        f.write(result.stderr.decode("utf-8"))

if __name__ == "__main__":
    filename_pdf = "03042018MA.pdf"
    download_pdf(filename_pdf)
    convert_pdf_to_txt(filename_pdf)
    upload_txt(filename_pdf)
