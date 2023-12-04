import fitz  # PyMuPDF
from PIL import Image

# Open the PDF
pdf_document = "./samples/SL65626-PFA.pdf"
pdf = fitz.open(pdf_document)

# Select a specific page (e.g., page 0)
page = pdf.load_page(0)
dpi=100
image = page.get_pixmap(dpi=dpi, alpha=False)
pdf.close()
#get the image from fitz
pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

#crop sections coords
section_1_coords = (34, 31, 163, 50)
section_2_coords = (34, 162, 579, 245)
section_3_coords = (34, 352, 789, 781)

#crop
section_1_image = pil_image.crop(section_1_coords)
section_2_image = pil_image.crop(section_2_coords)
section_3_image = pil_image.crop(section_3_coords)

recrop_section_2_coords = (0, 0, 456, 15)
section_2_width, section_2_height = section_2_image.size

#section_2_recrop = pil_image.crop(recrop_section_2_coords)

new_section_2_image = Image.new("RGB", (section_2_width, section_2_height), (255, 255, 255))
new_section_2_image.paste(section_2_image, (0, 0))
new_section_2_image.paste((255, 255, 255), recrop_section_2_coords)

#section_1_image.save("section1.jpg")
#new_section_2_image.save("section2.jpg")
#section_3_image.save("section3.jpg")


new_image_size = (800, 520)
new_image = Image.new("RGB", new_image_size, (255, 255, 255))

section_1_width, _ = section_1_image.size

# Paste the modified sections onto the new image
new_image.paste(section_1_image, (new_image_size[0] - 10 - section_1_width, 0))  # Example: Paste the cropped area
new_image.paste(new_section_2_image, (45, 5))
new_image.paste(section_3_image, (20, 85))

# Create a new image from the cropped region
image.save("cropped_image.png")
new_image.save("stitched_img.jpg")
