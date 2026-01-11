# Script that deletes any image that isn't part of the data needed 
# That includes any image that hasn't been extracted by hand in "eval"
import csv
import glob
import os

# paths
csv_dir = "data/eval"        
image_dir = "data/images"    

# get allowed images 
allowed = set()
csvs = glob.glob(f"{csv_dir}/*")
for csv in csvs:
    allowed.add(f"{os.path.splitext(os.path.basename(csv))[0]}.jpg")

# delete any images that aren't allowed
for filename in os.listdir(image_dir):
    if filename not in allowed:
        file_path = os.path.join(image_dir, filename)
        os.remove(file_path)
