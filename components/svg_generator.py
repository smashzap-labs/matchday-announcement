# components/svg_generator.py

import os
from pathlib import Path
import xml.etree.ElementTree as ET
from components.load import load_config

#from wand.image import Image
import cairosvg


def generate_match_list_svg(all_matches, base_filename):
    
    for sport, matches in matches_by_sport(all_matches).items():
        config_files_base = f'image_config_{sport}_*.json'
        config_files = list(Path('config').glob(config_files_base))

        for k, config_file in enumerate(config_files):

            svg_config = load_config(config_file)

            width = svg_config.get("width", 1080)
            height = svg_config.get("height", 1920)
            margin_top = svg_config.get("margin_top", 0)
            margin_bottom = svg_config.get("margin_bottom", 0)
            margin_left = svg_config.get("margin_left", 0)
            indent_right = svg_config.get("indent_right", 0)
            font_size_top = svg_config.get("font_size_top", 0)
            font_size_main = svg_config.get("font_size_main", 0)
            font_size_score = svg_config.get("font_size_score", 0)
            match_height = int(2.08*font_size_top + 2.08*font_size_main)
            background_path = svg_config.get("background_path", "")

            capacity = (height - margin_top - margin_bottom) // (match_height)
            if capacity < 1:
                capacity = 1

            chunks = [matches[i : i + capacity] for i in range(0, len(matches), capacity)]

            for i, chunk in enumerate(chunks):
                base, ext = os.path.splitext(base_filename)
                filename = f"{base}-{sport}-{k}-{i}{ext}"

                svg_elements = []
                svg_elements.append(
                    f'<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg version="1.1" id="svg1" xml:space="preserve" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect x="0" y="0" width="{width}" height="{height}" fill="#aaaaaa" />'
                )
                svg_elements.append(include_background_from_file(background_path))

                y_offset = margin_top

                for match in chunk:
                    # Background
                    svg_elements.append(
                        f'<rect x="{margin_left}" y="{y_offset}" width="{width - 2*margin_left}" height="{match_height}" fill="#fefefe" opacity=".9" rx="25" ry="25"/>'
                    )

                    # First Line
                    svg_elements.append(
                        f'<text x="{margin_left + 25}" y="{y_offset + font_size_top + 15}" font-size="{svg_config["font_size_top"]}" {svg_config["font_top"]} >'
                        f"{match.age_class.upper()} - {match.league.upper()}</text>"
                    )
                    
                    # Second Line
                    svg_elements.append(
                        f'<text x="{margin_left + 25}" y="{y_offset + 2.20*font_size_top + 15}" font-size="{svg_config["font_size_main"]}" {svg_config["font_main"]} >'
                        f"{match.home} {match.home_suffix}</text>"
                    )
                    svg_elements.append(
                        f'<text x="{margin_left + 25}" y="{y_offset + 2.20*font_size_top + 1.07*font_size_main + 15}" font-size="{svg_config["font_size_main"]}" {svg_config["font_main"]} >'
                        f"{match.away} {match.away_suffix}</text>"
                    )

                    if match.home_score != "" or match.away_score != "" or match.other != "":
                        # Result
                        svg_elements.append(
                            f'<text x="{width - indent_right}" y="{y_offset + match_height/2 + 0.1*font_size_score}" font-size="{svg_config["font_size_score"]}" {svg_config["font_score"]} >{match.home_score} : {match.away_score}</text>'
                            f'<text x="{width - indent_right}" y="{y_offset + match_height/2 + 1.01*font_size_score}" font-size="{svg_config["font_size_top"]}" {svg_config["font_score"]} >{match.other}</text>'
                        )
                    else:
                        # Time and Place
                        svg_elements.append(
                            f'<text x="{width - indent_right}" y="{y_offset + match_height/2 - 0.05*font_size_top}" font-size="{svg_config["font_size_top"]}" {svg_config["font_top"]} >'
                            f"{match.day}</text>"
                        )
                        svg_elements.append(
                            f'<text x="{width - indent_right}" y="{y_offset + match_height/2 + 1.00*font_size_top}" font-size="{svg_config["font_size_top"]}" {svg_config["font_top"]} >'
                            f"{match.time} Uhr</text>"
                        )

                    y_offset += 1.03*match_height

                svg_elements.append("</svg>")
                svg_data = "\n".join(svg_elements)

                # with open(f'{filename}.svg', "w", encoding="utf-8") as f:
                #     f.write(svg_data)

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