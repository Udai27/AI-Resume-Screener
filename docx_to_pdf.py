from docx2pdf import convert
import os

input_folder = "sample_resumes"
output_folder = "sample_resumes"

os.makedirs(output_folder, exist_ok=True)

convert(input_folder, output_folder)

print("All files converted successfully!")