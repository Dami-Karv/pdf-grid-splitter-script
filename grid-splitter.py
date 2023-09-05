import PyPDF2
from PyPDF2 import PageObject, Transformation
from copy import copy

def split_pdf(input_file, output_file):
    # Create a PDF reader and writer object
    pdf_reader = PyPDF2.PdfReader(input_file)
    pdf_writer = PyPDF2.PdfWriter()
    
    # Assuming the 9 pages are arranged in a 3x3 grid
    num_splits_vertical = 3
    num_splits_horizontal = 3
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        
        page_width = page.mediabox.width
        page_height = page.mediabox.height
        
        width_per_split = page_width / num_splits_horizontal
        height_per_split = page_height / num_splits_vertical
        
        # Crop and add each section of the combined page to the new PDF
        for y in reversed(range(num_splits_vertical)):     # Use reversed to count down
            for x in range(num_splits_horizontal):
                lower_left_x = x * width_per_split
                lower_left_y = y * height_per_split
                upper_right_x = (x + 1) * width_per_split
                upper_right_y = (y + 1) * height_per_split

                new_page = PageObject.create_blank_page(width=width_per_split, height=height_per_split)
                
                # Deep copy the original page for transformations
                page_copy = copy(page)
                page_copy.add_transformation(Transformation().translate(-lower_left_x, -lower_left_y))
                new_page.merge_page(page_copy)

                new_page.mediabox.lower_left = (0, 0)
                new_page.mediabox.upper_right = (width_per_split, height_per_split)

                pdf_writer.add_page(new_page)
    
    # Write the split pages to a new PDF file
    with open(output_file, 'wb') as output:
        pdf_writer.write(output)

# Usage
split_pdf('theoria.pdf', 'split.pdf')
