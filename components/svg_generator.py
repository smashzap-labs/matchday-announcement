# components/svg_generator.py

import os
import json
from wand.image import Image


def generate_match_list_svg(
    matches, base_filename, svg_config_path="components/image_config.json"
):
    """
    Erzeugt eine oder mehrere SVG-Dateien basierend auf der übergebenen Liste von Match-Objekten.
    Jede SVG hat exakt 1080px Breite und 1920px Höhe. Überschreitet die Anzahl der Spiele
    die Kapazität einer SVG, werden zusätzliche Dateien (mit Suffix "-1", "-2", etc.) erzeugt.

    Parameter:
      matches: Liste von Match-Objekten (müssen die Attribute day, time, age_class, league, home und away besitzen)
      base_filename: Basis-Dateiname für die SVG-Ausgabe
      svg_config_path: Pfad zur JSON-Konfiguration mit den SVG-Einstellungen
    """
    with open(svg_config_path, "r", encoding="utf-8") as f:
        svg_config = json.load(f)

    svg_width = svg_config.get("svg_width", 1080)
    svg_height = svg_config.get("svg_height", 1920)
    svg_margin = svg_config.get("svg_margin", 175)
    match_height = svg_config.get("match_height", 35)
    svg_background = svg_config.get(
        "svg_background",
        f'<rect width="{svg_width}" height="{svg_height}" fill="#ffffff" />',
    )

    capacity = (svg_height - svg_margin * 4) // (match_height * 4)
    if capacity < 1:
        capacity = 1

    chunks = [matches[i : i + capacity] for i in range(0, len(matches), capacity)]

    for i, chunk in enumerate(chunks):
        if i == 0:
            filename = base_filename
        else:
            base, ext = os.path.splitext(base_filename)
            filename = f"{base}-{i}{ext}"

        svg_elements = []
        svg_elements.append(
            f'<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg version="1.1" id="svg1" xml:space="preserve" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 285.74999 508">'
        )
        svg_elements.append(svg_background)

        y_offset = svg_margin

        for match in chunk:
            svg_elements.append(
                f'<rect x="25" y="{y_offset-10}" width="235" height="{match_height-3}" fill="#fefefe" opacity=".9" rx="5" ry="5"/>'
            )

            svg_elements.append(
                f'<text x="30" y="{y_offset}" {svg_config["font_top"]} >'
                f"{match.age_class} - {match.league}</text>"
            )
            svg_elements.append(
                f'<text x="{svg_width/4 - 60}px" y="{y_offset + 10}" {svg_config["font_top"]} >'
                f"{match.day}</text>"
            )
            svg_elements.append(
                f'<text x="{svg_width/4 - 60}px" y="{y_offset + 18}" {svg_config["font_top"]} >'
                f"{match.time} Uhr</text>"
            )

            # Zweite Zeile: Groß "Heimverein : Gastverein"
            svg_elements.append(
                f'<text x="40" y="{y_offset + 12}" {svg_config["font_main"]} >'
                f"{match.home} {match.home_suffix}</text>"
            )
            svg_elements.append(
                f'<text x="40" y="{y_offset + 26}" {svg_config["font_main"]} >'
                f"{match.away} {match.away_suffix}</text>"
            )

            # Platzhalter für das Ergebnis rechts
            # svg_elements.append(
            #     f'<text x="{svg_width/4 - 70}px" y="{y_offset + 16}" {svg_config["font_score"]} >10 : 10 </text>'
            # )

            y_offset += match_height

        svg_elements.append("</svg>")
        svg_data = "\n".join(svg_elements)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(svg_data)

        svg_to_png_with_wand(svg_data, filename)


def svg_to_png_with_wand(svg_data, output_filename):
    # Stelle sicher, dass svg_data als Bytes vorliegt
    svg_bytes = svg_data.encode("utf-8") if isinstance(svg_data, str) else svg_data
    with Image(blob=svg_bytes, format="svg") as img:
        img.format = "png"
        img.save(filename=output_filename + ".png")
