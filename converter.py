import csv
from dataclasses import dataclass

from pyproj import CRS, Transformer


IN_CSV = r"C:\Users\m.rahman\arcgis\xlsxToShapefile\data\WCMA-Waterway-crossings.csv"
OUT_CSV = r"C:\Users\m.rahman\arcgis\xlsxToShapefile\data\crossings_latlon.csv"


@dataclass(frozen=True)
class Candidate:
    zone: int
    lon: float
    lat: float


def _make_transformer(mga_zone: int) -> Transformer:
    if mga_zone == 54:
        src = CRS.from_epsg(7854)
    elif mga_zone == 55:
        src = CRS.from_epsg(7855)
    else:
        raise ValueError(f"Unsupported MGA zone: {mga_zone}")
    dst = CRS.from_epsg(7844)
    return Transformer.from_crs(src, dst, always_xy=True)


_T54 = _make_transformer(54)
_T55 = _make_transformer(55)


def _score_for_wimmera(c: Candidate) -> float:
    target_lon = 142.0
    target_lat = -36.7
    return (c.lon - target_lon) ** 2 + (c.lat - target_lat) ** 2


def _within_vic_bounds(lon: float, lat: float) -> bool:
    return 140.0 <= lon <= 150.0 and -39.5 <= lat <= -33.5


def _pick_zone(easting: float, northing: float) -> Candidate:
    lon54, lat54 = _T54.transform(easting, northing)
    lon55, lat55 = _T55.transform(easting, northing)

    c54 = Candidate(zone=54, lon=lon54, lat=lat54)
    c55 = Candidate(zone=55, lon=lon55, lat=lat55)

    ok54 = _within_vic_bounds(c54.lon, c54.lat)
    ok55 = _within_vic_bounds(c55.lon, c55.lat)

    if ok54 and not ok55:
        return c54
    if ok55 and not ok54:
        return c55
    if ok54 and ok55:
        return min((c54, c55), key=_score_for_wimmera)

    return min((c54, c55), key=_score_for_wimmera)


def main() -> None:
    with open(IN_CSV, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("Input CSV has no header row")

        required = {"Center X", "Center Y"}
        missing = sorted(required - set(reader.fieldnames))
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        out_fieldnames = list(reader.fieldnames)
        out_fieldnames.extend(["Longitude", "Latitude", "MGA_Zone"])

        rows = []
        for r in reader:
            x_raw = (r.get("Center X") or "").strip()
            y_raw = (r.get("Center Y") or "").strip()

            if x_raw == "" or y_raw == "":
                r["Longitude"] = ""
                r["Latitude"] = ""
                r["MGA_Zone"] = ""
                rows.append(r)
                continue

            easting = float(x_raw)
            northing = float(y_raw)

            c = _pick_zone(easting, northing)
            r["Longitude"] = f"{c.lon:.8f}"
            r["Latitude"] = f"{c.lat:.8f}"
            r["MGA_Zone"] = str(c.zone)
            rows.append(r)

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to: {OUT_CSV}")


if __name__ == "__main__":
    main()
