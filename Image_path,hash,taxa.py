import os
import csv
import pandas as pd
from PIL import Image
import imagehash
from concurrent.futures import ThreadPoolExecutor, as_completed#???
from multiprocessing import cpu_count#???

root_folder = '/Users/vidhu/Library/CloudStorage/Box-Box/planktonROIs/20250609_Export-MAZOOPS_ZooScan'
output_csv = 'plankton_images.csv'

def perceptual_hash(filepath):
    try:
        with Image.open(filepath) as img:
            return str(imagehash.phash(img))
    except Exception as e:
        print(f"Error hashing {filepath}: {e}")
        return ''

def find_tsv_file(folder):
    for file in os.listdir(folder):
        if file.lower().endswith('.tsv'):
            return os.path.join(folder, file)
    return None

image_data = []

# Loop through all subbys of root
subfolders = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]
subfolders.sort()  # For consistent order

for subfolder in subfolders:
    subfolder_path = os.path.join(root_folder, subfolder)
    print(f"\nProcessing subfolder: {subfolder_path}")

    tsv_file = find_tsv_file(subfolder_path)
    if tsv_file:
        print(f"Found TSV file: {tsv_file}")
        try:
            df = pd.read_csv(tsv_file, sep='\t')
            df.columns = [col.strip() for col in df.columns]

            image_col = 'img_file_name'
            taxa_col = 'object_annotation_category'

            if image_col not in df.columns:
                print(f"Error: TSV file is missing the expected image filename column '{image_col}'.")
                continue
            if taxa_col not in df.columns:
                print(f"Error: TSV file is missing the expected taxa column '{taxa_col}'.")
                continue

            img_to_taxa = {}
            for _, row in df.iterrows():
                img_name_in_tsv = str(row[image_col]).strip()
                taxa_value = str(row[taxa_col]).strip()
                img_to_taxa[img_name_in_tsv] = taxa_value

            actual_image_files = [
                file
                for file in os.listdir(subfolder_path)
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))
            ]
            print(f"Found {len(actual_image_files)} image files in the folder.")

            items_to_process = []
            for file_name_in_folder in actual_image_files:
                img_path = os.path.join(subfolder_path, file_name_in_folder)
                items_to_process.append((img_path, file_name_in_folder))

            with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
                future_to_filename = {
                    executor.submit(perceptual_hash, item[0]): item[1]
                    for item in items_to_process
                }

                for future in as_completed(future_to_filename):
                    original_filename = future_to_filename[future]
                    img_full_path = os.path.join(subfolder_path, original_filename)
                    hash_val = future.result()
                    taxa = img_to_taxa.get(original_filename, '')
                    if not taxa:
                        print(f"Warning: No taxa found in TSV for image {original_filename}. Taxa column will be empty for this image.")
                    row = [img_full_path, hash_val, taxa]
                    image_data.append((taxa, row))

        except Exception as e:
            print(f"An error occurred while processing the TSV or images: {e}")
    else:
        print(f"No TSV file found in the subfolder: {subfolder_path}. Taxa column will be empty.")
image_data.sort(key=lambda x: x[0].lower() if x[0] else '')
if image_data:
    header = ['image_path', 'hash', 'taxa']
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for _, row in image_data:
            writer.writerow(row)
    print(f"\nCSV saved as {output_csv} with {len(image_data)} entries.")
else:
    print("\nNo img processed or no data to write to CSV.")
