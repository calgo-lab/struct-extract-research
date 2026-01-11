# Script that turns .jpg images into PDFs
import glob
import os
import pymupdf

# paths
image_dir = "data/images"
pdf_dir = "data/pdfs"

# convert images to pdfs and save
images = glob.glob(f"{image_dir}/*")
for image in images:
    name = os.path.splitext(os.path.basename(image))[0]
    jpg = pymupdf.open(image)
    pdfbytes = jpg.convert_to_pdf()
    pdf = pymupdf.open("pdf", pdfbytes)
    pdf.save(f"{pdf_dir}/{name}.pdf")
