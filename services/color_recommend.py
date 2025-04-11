import pandas as pd
import seaborn as sns
import random
import colorsys
from matplotlib.colors import to_rgb, to_hex
import os

this_dir = os.path.dirname(__file__)

# Define palette name to color map (Seaborn palettes)
PALETTE_MAP = {
    "muted": sns.color_palette("muted").as_hex(),
    "bright": sns.color_palette("bright").as_hex(),
    "dark": sns.color_palette("dark").as_hex(),
    "pastel": sns.color_palette("pastel").as_hex(),
    "colorblind": sns.color_palette("colorblind").as_hex(),
    "vibrant": sns.color_palette("Set2").as_hex(),
    "bold": sns.color_palette("tab10").as_hex(),
}

# Load occasion to palette name mapping from CSV
def load_palette_mapping():
    df = pd.read_csv(os.path.join(this_dir, "../dataSets/occasion_color_palettes.csv"))
    return dict(zip(df['occasion'], df['palette']))

# Color harmony functions
def get_complementary_color(hex_color):
    r, g, b = to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h_complementary = (h + 0.5) % 1.0
    r_c, g_c, b_c = colorsys.hls_to_rgb(h_complementary, l, s)
    return to_hex((r_c, g_c, b_c))

def get_analogous_color(hex_color):
    r, g, b = to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h_analogous = (h + 0.08) % 1.0
    r_a, g_a, b_a = colorsys.hls_to_rgb(h_analogous, l, s)
    return to_hex((r_a, g_a, b_a))

def get_triadic_color(hex_color):
    r, g, b = to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h_triadic = (h + 1/3) % 1.0
    r_t, g_t, b_t = colorsys.hls_to_rgb(h_triadic, l, s)
    return to_hex((r_t, g_t, b_t))

# assign 1 recommended color
def assign_color_code_by_occasion(item, occasion_palette_map, palette_colors):
    for occ in item.get("occasions", []):
        if occ in occasion_palette_map:
            palette_name = occasion_palette_map[occ]
            colors = palette_colors.get(palette_name)
            if colors:
                base_color = random.choice(colors)
                mode = random.choice(["complementary", "analogous", "triadic"])
                if mode == "complementary":
                    return get_complementary_color(base_color)
                elif mode == "analogous":
                    return get_analogous_color(base_color)
                elif mode == "triadic":
                    return get_triadic_color(base_color)
    # fallback color
    return random.choice(palette_colors["muted"])

def apply_recommended_colors(items):
    occasion_palette_map = load_palette_mapping()
    for item in items:
        item["colorCode"] = assign_color_code_by_occasion(
            item, occasion_palette_map, PALETTE_MAP
        )
    return items
