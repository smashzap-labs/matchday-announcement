# components/svg_generator.py

import os
from pathlib import Path
import xml.etree.ElementTree as ET
from components.load import load_config
import cairosvg

def generate_match_list_svg(all_matches, base_filename, svg_export=False):
    
    for sport, matches in matches_by_sport(all_matches).items():
        config_files = list(Path('config').glob('image_config_*.json'))

        for k, config_file in enumerate(config_files):

            svg_config = load_config(config_file)
            content = svg_config.get("content", "")
            width = svg_config.get("width", 1080)
            height = svg_config.get("height", 1920)
            capacity = svg_config.get("capacity", 20)
            match_height = svg_config.get("match_height", 100)
            background_path = svg_config.get(f'background_path_{sport}', "")

            chunks = [matches[i : i + capacity] for i in range(0, len(matches), capacity)]

            for i, chunk in enumerate(chunks):
                y_offset = svg_config.get("y_offset", 10)
                base, ext = os.path.splitext(base_filename)
                filename = f"{base}-{k}-{sport}-{i}{ext}"

                svg_elements = []
                svg_elements.append(
                    f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                            <svg version="1.1" id="svg1" xml:space="preserve" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
                                <rect x="0" y="0" width="{width}" height="{height}" fill="#aaaaaa" />'''
                )
                svg_elements.append(include_background_from_file(background_path))

                for match in chunk:
                    # insert the match data into the SVG content like given in config
                    svg_elements.append(eval(f"f'''{content}'''"))
                    y_offset += 1.03*match_height

                svg_elements.append("</svg>")
                svg_data = "\n".join(svg_elements)

                if (svg_export):
                    # Save the SVG data to a file
                    with open(f'{filename}.svg', "w", encoding="utf-8") as f:
                        f.write(svg_data)

                # Save the SVG data as PNG
                cairosvg.svg2png(bytestring=svg_data.encode("utf-8"), write_to=filename)

def include_background_from_file(background_path):
    """
    Lädt die SVG-Datei vom angegebenen Pfad, entfernt das äußere <svg>-Tag
    und gibt den inneren XML-Content (als String) zurück.
    """
    if not os.path.exists(background_path):
        return ""
    tree = ET.parse(background_path)
    root = tree.getroot()
    inner_content = "".join(ET.tostring(child, encoding="unicode") for child in root)
    return inner_content

def matches_by_sport(matches):
    matches_by_sport = {}
    for match in matches:
        sport = match.sport
        if sport not in matches_by_sport:
            matches_by_sport[sport] = []
        matches_by_sport[sport].append(match)
    return matches_by_sport