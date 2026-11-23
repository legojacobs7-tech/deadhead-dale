import sys, glob
from PIL import Image
fs = sorted(glob.glob(sys.argv[1])); cols = int(sys.argv[3]) if len(sys.argv) > 3 else 7
w, h = 216, 384; rows = (len(fs) + cols - 1) // cols
s = Image.new("RGB", (w * cols, h * rows), "white")
for i, f in enumerate(fs): s.paste(Image.open(f).convert("RGB").resize((w, h)), ((i % cols) * w, (i // cols) * h))
s.save(sys.argv[2])
