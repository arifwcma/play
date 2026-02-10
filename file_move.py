import os
import shutil

root_folder = r"C:\Users\m.rahman\gis_data\stawell\rasters"

for sub in os.listdir(root_folder):
    sub_path = os.path.join(root_folder, sub)
    if os.path.isdir(sub_path):
        tif_path = os.path.join(sub_path, "data.tif")
        if os.path.exists(tif_path):
            new_name = f"{sub}.tif"
            new_path = os.path.join(root_folder, new_name)
            shutil.move(tif_path, new_path)
