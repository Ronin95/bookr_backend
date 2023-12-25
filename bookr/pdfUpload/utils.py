import os
from PyPDF2 import PdfReader, PdfWriter
from django.conf import settings

def split_pdf(file_path): # split pdf after upload
    pdf_reader = PdfReader(file_path)
    num_pages = len(pdf_reader.pages)
    file_size_kb = os.path.getsize(file_path) / 512
    file_base_name = os.path.basename(file_path).replace('.pdf', '')

    # Determine the number of splits based on file size
    splits = int(file_size_kb // 1000) + 1
    splits = min(splits, 10)  # Limit to a maximum of 10 splits

    pages_per_split = num_pages // splits
    remaining_pages = num_pages % splits

    for i in range(splits):
        start_page = i * pages_per_split
        end_page = (i + 1) * pages_per_split
        if i == splits - 1:
            end_page += remaining_pages  # Add any remaining pages to the last split

        output_filename = f"{file_base_name}_P{i + 1}.pdf"
        output_path = os.path.join(settings.MEDIA_ROOT, 'splitUpPDFs', output_filename)

        pdf_writer = PdfWriter()
        for page_num in range(start_page, end_page):
            pdf_page = pdf_reader.pages[page_num]
            pdf_writer.add_page(pdf_page)

        with open(output_path, 'wb') as output_pdf_file:
            pdf_writer.write(output_pdf_file)

