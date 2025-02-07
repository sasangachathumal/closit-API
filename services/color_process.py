import colorsys


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb_color):
    return "#{:02x}{:02x}{:02x}".format(*rgb_color)


def is_close_to_white(rgb):
    r, g, b = rgb
    return (r > 240 and g > 240 and b > 240)


def is_close_to_black(rgb):
    r, g, b = rgb
    return (r < 15 and g < 15 and b < 15)


def get_matching_colors(data):
    hex_color = data["color"]
    # Convert hex to RGB
    rgb = hex_to_rgb(hex_color)
    # Convert RGB to HSV
    hsv = colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)

    # Complementary color
    complementary_hue = (hsv[0] + 0.5) % 1.0
    complementary_rgb = colorsys.hsv_to_rgb(complementary_hue, hsv[1], hsv[2])
    complementary_rgb = tuple(int(c * 255) for c in complementary_rgb)

    # Analogous colors
    analogous_hues = [(hsv[0] + 0.083) % 1.0, (hsv[0] - 0.083) % 1.0]  # ±30°
    analogous_colors = [
        tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, hsv[1], hsv[2]))
        for hue in analogous_hues
    ]

    # Triadic colors
    triadic_hues = [(hsv[0] + 1 / 3) % 1.0, (hsv[0] + 2 / 3) % 1.0]  # ±120°
    triadic_colors = [
        tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, hsv[1], hsv[2]))
        for hue in triadic_hues
    ]

    # Check for edge cases
    if is_close_to_white(rgb):
        edge_case_colors = [(0, 0, 0), (50, 50, 50)]  # Black or darker grays
    elif is_close_to_black(rgb):
        edge_case_colors = [(255, 255, 255), (200, 200, 200)]  # White or lighter grays
    else:
        edge_case_colors = []

    # Combine all matching colors
    matching_colors = [complementary_rgb] + analogous_colors + triadic_colors + edge_case_colors

    # Convert to hex and return
    return {"matching_colors": {
        "complementary_rgb": [complementary_rgb],
        "analogous_colors": analogous_colors,
        "triadic_colors": triadic_colors,
        "edge_case_colors": edge_case_colors
    }}, 200
    # return [rgb_to_hex(color) for color in matching_colors]


# Example usage
# input_color = "#FF5733"  # Hex input
# matching_colors = get_matching_colors(input_color)
# print(f"Input color: {input_color}")
# print(f"Matching colors: {matching_colors}")
