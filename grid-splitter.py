import PyPDF2
from PyPDF2 import PageObject, Transformation
from copy import copy

def split_pdf(input_file, output_file):
    valid_splits = [2, 4, 6, 8, 9, 16]
    num_splits = int(input(f"Enter the number of splits per page {valid_splits}: "))
    
    while num_splits not in valid_splits:
        print(f"Invalid input! Please enter one of {valid_splits}")
        num_splits = int(input(f"Enter the number of splits per page {valid_splits}: "))
    
    if num_splits == 2 or num_splits == 6:
        num_splits_horizontal = 2
        num_splits_vertical = num_splits // 2
    else:
        num_splits_horizontal = int(num_splits ** 0.5)
        num_splits_vertical = num_splits // num_splits_horizontal
    
    pdf_reader = PyPDF2.PdfReader(input_file)
    pdf_writer = PyPDF2.PdfWriter()

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        
        page_width = page.mediabox.width
        page_height = page.mediabox.height
        
        width_per_split = page_width / num_splits_horizontal
        height_per_split = page_height / num_splits_vertical
        
        for y in reversed(range(num_splits_vertical)):
            for x in range(num_splits_horizontal):
                lower_left_x = x * width_per_split
                lower_left_y = y * height_per_split
                upper_right_x = (x + 1) * width_per_split
                upper_right_y = (y + 1) * height_per_split

                new_page = PageObject.create_blank_page(width=width_per_split, height=height_per_split)
                page_copy = copy(page)
                page_copy.add_transformation(Transformation().translate(-lower_left_x, -lower_left_y))
                new_page.merge_page(page_copy)

                new_page.mediabox.lower_left = (0, 0)
                new_page.mediabox.upper_right = (width_per_split, height_per_split)

                pdf_writer.add_page(new_page)

    with open(output_file, 'wb') as output:
        pdf_writer.write(output)

input_file = input("Enter the path of the input PDF file: ")
output_file = input("Enter the path of the output PDF file: ")

split_pdf(input_file, output_file)
