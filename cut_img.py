from pathlib import Path
from os import listdir
from PIL import Image, ImageChops

input_path = Path(r"P:\Wärmeplanung\01_Intern-Methodik\03_Bearbeitung\02_Vorlagen_Bearbeitung\Veröffentlichung nach dem WPG\In Entwicklung\Zielszenario\V1.5\Export_Zielszenario\Zielszenario_Diagramme neu 5.png")

files = [file for file in listdir(Path(__file__).parent) if file[-4:] == ".png"]
print(files)


def cut_img(path: Path):

    if not path.exists():
        raise FileNotFoundError(f"Bild nicht gefunden:\n{path}")

    img = Image.open(path).convert("RGB")

    bounds = (10,10, img.width -10, img.height -10)
    img = img.crop(bounds)

    # Fast-weiße Pixel ebenfalls als Hintergrund behandeln
    tolerance = 10
    bg = Image.new("RGB", img.size, "white")
    diff = ImageChops.difference(img, bg).convert("L")

    # Nur deutlich vom Weiß abweichende Pixel berücksichtigen
    mask = diff.point(lambda pixel: 255 if pixel > tolerance else 0)
    bbox = mask.getbbox()

    if bbox:
        left, top, right, bottom = bbox
        margin = 20

        crop_box = (
            max(0, left - margin),
            max(0, top - margin),
            min(img.width, right + margin),
            min(img.height, bottom + margin),
        )

        cropped = img.crop(crop_box)
        cropped.save(path)

        print(f"Gespeichert unter: {path}")
        print(f"Ausschnitt: {crop_box}")
    else:
        print("Keine vom weißen Hintergrund abweichenden Pixel gefunden.")

for f in files:
    cut_img(Path(__file__).parent / f)