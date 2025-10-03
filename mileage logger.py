import os
from datetime import datetime, date
import googlemaps

API_KEY = ""
gmaps   = googlemaps.Client(key=API_KEY)

LOCATIONS = {
    "Antrim Area Hospital": "Antrim Area Hospital, Antrim, Northern Ireland",
    "Bellaghy":             "Bellaghy, Northern Ireland",
    "Coagh":                "Coagh, Northern Ireland",
    "Draperstown":          "Draperstown, Northern Ireland",
    "Cookstown":            "Cookstown, Northern Ireland",
    "Maghera":              "Maghera, Northern Ireland",
    "Magherafelt":          "Magherafelt, Northern Ireland",
    "Randalstown":          "Randalstown, Northern Ireland",
    "Arboe":                "Arboe, Northern Ireland",
    "Ballymoney":           "Ballymoney, Northern Ireland",
    "Ballymena":            "Ballymena, Northern Ireland",
}
NAME_MAP = {name.lower(): name for name in LOCATIONS}

def get_miles(a, b):
    result = gmaps.distance_matrix(a, b, mode="driving", units="imperial")
    elem   = result["rows"][0]["elements"][0]
    if elem["status"] != "OK":
        raise RuntimeError(f"No route: {elem['status']}")
    return float(elem["distance"]["text"].split()[0])

def prompt_month_year():
    month_name = input("Enter month (e.g. October): ").strip().capitalize()
    month_num  = datetime.strptime(month_name, "%B").month
    return month_name, month_num, date.today().year

def ensure_output_file(month, year):
    folder = os.path.expanduser("~/Documents/mileage")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{month}_{year}_mileage.txt")
    print(f"Logging to {path}\n")
    return path

def log_day_trips(path, month_name, month_num, year):
    home = "Antrim Area Hospital"
    while True:
        day = input(f"Enter day for {month_name} {year} (dd) or EXIT: ").strip()
        if day.upper() == "EXIT":
            print("Goodbye.")
            break
        if not day.isdigit() or not (1 <= int(day) <= 31):
            print("  → Please enter a valid day number (1–31).")
            continue

        trip_date = f"{int(day):02d}/{month_num:02d}/{year}"
        current   = home
        segments  = []
        total     = 0.0

        while True:
            dest_in = input(f"Next from {current} (DONE to finish): ").strip().lower()
            if dest_in.upper() == "DONE":
                break
            if dest_in not in NAME_MAP:
                print("  → Unknown place, try again.")
                continue

            dest  = NAME_MAP[dest_in]
            miles = get_miles(LOCATIONS[current], LOCATIONS[dest])
            segments.append((current, dest, miles))
            total += miles
            print(f"    logged {round(miles)} mi → total {round(total)} mi")
            current = dest

        if current != home:
            ret = get_miles(LOCATIONS[current], LOCATIONS[home])
            segments.append((current, home, ret))
            total += ret
            print(f"    return leg {round(ret)} mi")

        business   = round(total)
        allowance  = 50
        full_total = business + allowance

        with open(path, "a", encoding="utf-8") as f:
            f.write(f"Date: {trip_date}\n")
            f.write("Home → Hospital: 25 mi\n")
            for o, d, m in segments:
                f.write(f"{o} → {d}: {round(m)} mi\n")
            f.write("Hospital → Home: 25 mi\n")
            f.write(f"Business mileage: {business} mi\n")
            f.write(f"Total with allowance: {full_total} mi\n")
            f.write("-" * 30 + "\n")

        print(f"\n— {trip_date} summary —")
        print("Home → Hospital: 25 mi")
        for o, d, m in segments:
            print(f"{o} → {d}: {round(m)} mi")
        print("Hospital → Home: 25 mi")
        print(f"Business: {business} mi; Total: {full_total} mi\n")

def main():
    month_name, month_num, year = prompt_month_year()
    path = ensure_output_file(month_name, year)
    log_day_trips(path, month_name, month_num, year)

if __name__ == "__main__":
    main()

