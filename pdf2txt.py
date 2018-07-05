import os.path
import subprocess

def convert_pdf_to_txt(dir_pdf, dir_txt, dir_log, filename_pdf):
    filename_txt = filename_pdf[:-4] + ".txt"
    result = subprocess.run([
        "java", "-jar", "pdfbox-app-2.0.11.jar", "ExtractText", "-debug", 
        os.path.join(dir_pdf, filename_pdf),
        os.path.join(dir_txt, filename_txt)
        ], 

        stderr=subprocess.PIPE)

    filename_log = filename_pdf[:-4] + ".log"
    with open(os.path.join(dir_log, filename_log), "w") as f:
        f.write(result.stderr.decode("utf-8"))

if __name__ == "__main__":
    dir_pdf = "./data"
    dir_txt = "./txt"
    dir_log = "./log"
    filename_pdf = "03042018_122TRF1.pdf"
    convert_pdf_to_txt(dir_pdf, dir_txt, dir_log, filename_pdf)
