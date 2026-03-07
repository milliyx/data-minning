"""Generate a screenshot image listing all parquet files in data/bronze."""
from PIL import Image, ImageDraw
import os

folder = "data/bronze"
if not os.path.isdir(folder):
    raise FileNotFoundError(folder)

files = os.listdir(folder)
text = "\n".join(files)
img = Image.new("RGB", (400, 200), color="white")
draw = ImageDraw.Draw(img)
draw.text((10, 10), text, fill="black")
img_path = os.path.join(folder, "files_screenshot.png")
img.save(img_path)
print(f"Screenshot saved to {img_path}")
