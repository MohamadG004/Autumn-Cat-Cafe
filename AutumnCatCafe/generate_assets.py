"""
generate_assets.py
Generates PNG sprite assets programmatically with Pillow.
Called automatically by main.py if assets are missing,
or run standalone:  python generate_assets.py
"""
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


def _ensure_dirs():
    for sub in ("characters", "backgrounds", "ui", "icons",
                "particles", "audio", "decorations"):
        os.makedirs(os.path.join(ASSETS_DIR, sub), exist_ok=True)


def _try_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFilter
        return Image, ImageDraw, ImageFilter
    except ImportError:
        return None, None, None


def generate_leaf_sprites(Image, ImageDraw):
    """Generate 6 autumn leaf PNGs."""
    colors = [
        (208, 98,  28),
        (184, 72,  22),
        (228, 148, 38),
        (158, 52,  18),
        (198, 128, 48),
        (220, 100, 40),
    ]
    for i, col in enumerate(colors):
        img  = Image.new("RGBA", (40, 40), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([2, 12, 38, 28], fill=(*col, 220))
        draw.line([(20, 12), (30, 30)], fill=(*col, 180), width=1)
        path = os.path.join(ASSETS_DIR, "particles", f"leaf_{i}.png")
        img.save(path)


def generate_coin_icon(Image, ImageDraw):
    img  = Image.new("RGBA", (48, 48), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 2, 46, 46], fill=(224, 164, 42, 255))
    draw.ellipse([8, 8, 40, 40], fill=(238, 198, 88, 255))
    draw.text((16, 12), "¥", fill=(185, 128, 24, 255))
    img.save(os.path.join(ASSETS_DIR, "icons", "coin.png"))


def generate_all_assets():
    _ensure_dirs()
    Image, ImageDraw, ImageFilter = _try_pillow()
    if Image is None:
        print("[generate_assets] Pillow not found – skipping PNG generation.")
        print("  Install with:  pip install Pillow")
        return

    generate_leaf_sprites(Image, ImageDraw)
    generate_coin_icon(Image, ImageDraw)
    print("[generate_assets] Assets generated successfully.")


if __name__ == "__main__":
    generate_all_assets()
