# Ensure you have inkscape installed to run this
import os
import re
from pathlib import Path
import subprocess

# CONFIG
SVG_INPUT_PATH = "DVD_logo.svg"
OUTPUT_FOLDER = "generated_pngs"
COLORS = {
    "red": "#FF0000",
    "green": "#00FF00",
    "blue": "#0000FF",
    "yellow": "#FFFF00",
    "magenta": "#FF00FF",
    "cyan": "#00FFFF",
    "white": "#FFFFFF",
    "orange": "#FFA500",
    "salmonpink": "#E1A5A5",
    "wistful": "#9F99C3",
    "darkred": "#5E1111",
    "springgreen": "#34A569",
    "purple": "#8F3D90",
}

INKSCAPE_CMD = r"C:\Program Files\Inkscape\bin\inkscape.exe"  # Change path to your correct inkscape executable

# Ensure output folder exists
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

# Remove old PNGs
for f in Path(OUTPUT_FOLDER).glob("dvd_*.png"):
    f.unlink()

# Read base SVG
with open(SVG_INPUT_PATH, "r", encoding="utf-8") as f:
    original_svg = f.read()

# Generate PNGs
for name, hex_color in COLORS.items():
    temp_svg_path = os.path.join(OUTPUT_FOLDER, f"dvd_{name}.svg")
    output_png_path = os.path.join(OUTPUT_FOLDER, f"dvd_{name}.png")

    # Step 1: Start from the base SVG
    modified_svg = original_svg

    # Step 2: Force replace all existing fills (inline or style)
    modified_svg = re.sub(r'fill="[^"]*"', f'fill="{hex_color}"', modified_svg)
    modified_svg = re.sub(r'fill:[^;"]*', f'fill:{hex_color}', modified_svg)

    # Step 3: Inject fill if it's missing from <path> tags
    modified_svg = re.sub(
        r'<path(?![^>]*fill=)',
        f'<path fill="{hex_color}"',
        modified_svg
    )

    # Write modified SVG
    with open(temp_svg_path, "w", encoding="utf-8") as f:
        f.write(modified_svg)

    # Export to PNG with transparent background
    try:
        result = subprocess.run([
            INKSCAPE_CMD,
            temp_svg_path,
            "--export-type=png",
            "--export-background=none",
            "--export-background-opacity=0",
            f"--export-filename={output_png_path}"
        ], check=True, capture_output=True, text=True)
        print(f"Generated {output_png_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate {output_png_path}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
