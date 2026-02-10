import json
import xml.etree.ElementTree as ET

lyrx_path = r"C:\Users\m.rahman\qgis\land_use_report\data\original\clum_50m_2023_v2\Land use, simplified.lyrx"
qml_path = r"C:\Users\m.rahman\qgis\land_use_report\data\original\clum_50m_2023_v2\Land use, simplified.qml"
qml_out = r"C:\Users\m.rahman\qgis\land_use_report\data\original\clum_50m_2023_v2\Land use, simplified_updated.qml"

def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level + 1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

with open(lyrx_path, "r", encoding="utf-8") as f:
    lyrx = json.load(f)

colorizer = lyrx["layerDefinitions"][0]["colorizer"]
entries = []

for g in colorizer["groups"]:
    for c in g["classes"]:
        label = c["label"]
        rgb = c["color"]["values"]
        for v in c["values"]:
            hex_color = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
            entries.append({"value": v, "color": hex_color, "label": label})

tree = ET.parse(qml_path)
root = tree.getroot()

palette = root.find(".//colorPalette")
if palette is not None:
    palette.clear()
else:
    palette = ET.SubElement(root.find(".//rasterrenderer"), "colorPalette")

for e in entries:
    ET.SubElement(
        palette,
        "paletteEntry",
        value=str(e["value"]),
        color=e["color"],
        alpha="255",
        label=e["label"],
    )

indent(root)
tree.write(qml_out, encoding="utf-8", xml_declaration=True)
print("Updated QML saved:", qml_out)
