import argparse
from pdf2image import convert_from_path
from PIL import Image
import os

def convert_pdf_to_images(pdf_path, output_folder='./output', max_size_mb=4.5, dpi=800):
    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF to a list of images
    images = convert_from_path(pdf_path, dpi=dpi)

    for i, image in enumerate(images):
        # Define the output file path
        output_file = os.path.join(output_folder, f'page_{i + 1}.jpg')

        # Save the image
        image.save(output_file, 'JPEG', quality=100)

        # Check the file size and adjust quality if necessary
        while os.path.getsize(output_file) > max_size_mb * 1024 * 1024:
            with Image.open(output_file) as img:
                # Reduce the quality by 5 each iteration if the file size exceeds the limit
                quality = int(img.info.get('quality', 85) * 0.95)
                img.save(output_file, 'JPEG', quality=quality)

    print(f"PDF conversion completed. Images saved in '{output_folder}' folder.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to images")
    parser.add_argument('pdf_path', type=str, help="Path to the PDF file")
    parser.add_argument('--output_folder', type=str, default='./output', help="Output folder for images")
    parser.add_argument('--max_size_mb', type=str, default='5', help="Max size for each output image in MB")
    parser.add_argument('--dpi', type=int, default=800, help="DPI for the images")

    args = parser.parse_args()

    convert_pdf_to_images(args.pdf_path, args.output_folder, args.max_size_mb, args.dpi)
