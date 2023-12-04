import fitz  # PyMuPDF
from PIL import Image
from pathlib import Path
from datetime import datetime
import re

pdf_folder = "./samples/"
path = Path(pdf_folder)

def report_stiching(file, backup_folder):

    file_name = file.stem

    pdf = fitz.open(file)

    page = pdf.load_page(0)
    dpi=100
    image = page.get_pixmap(dpi=dpi, alpha=False)
    pdf.close()
    
    # get the image from fitz
    pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

    # crop sections coords
    section_1_coords = (34, 31, 163, 50)
    section_2_coords = (34, 162, 579, 245)
    section_3_coords = (34, 352, 789, 781)

    # crop
    section_1_image = pil_image.crop(section_1_coords)
    section_2_image = pil_image.crop(section_2_coords)
    section_3_image = pil_image.crop(section_3_coords)

    # recrop one of the sections, to remove irrelevant info
    recrop_section_2_coords = (0, 0, 456, 15)
    section_2_width, section_2_height = section_2_image.size

    # create a new blank image and paste a blank section recrop on top of the section
    new_section_2_image = Image.new("RGB", (section_2_width, section_2_height), (255, 255, 255))
    new_section_2_image.paste(section_2_image, (0, 0))
    new_section_2_image.paste((255, 255, 255), recrop_section_2_coords)

    # create a new image from the cropped region
    new_image_size = (800, 520)
    new_image = Image.new("RGB", new_image_size, (255, 255, 255))

    section_1_width, _ = section_1_image.size

    # Paste the modified sections onto the new image
    new_image.paste(section_1_image, (new_image_size[0] - 10 - section_1_width, 0))  # Example: Paste the cropped area
    new_image.paste(new_section_2_image, (45, 5))
    new_image.paste(section_3_image, (20, 85))


    # regular expression to get folder name from file
    pattern = r'[ _-]'
    folder_name = re.split(pattern, file_name)

    current_year = datetime.today().year

    backup_dir = backup_folder / str(current_year) / folder_name[0]

    backup_dir.mkdir(parents=True, exist_ok=True)

    file_path = backup_dir / (file_name + ".jpg")

    new_image.save(file_path)




for file in path.iterdir():
    if file.is_file() and file.suffix.lower() == '.pdf':
        report_stiching(file, path)