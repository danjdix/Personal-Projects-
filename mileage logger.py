import googlemaps
import sys 
import time
import re 

API_KEY = "" # enter api key

gmaps = googlemaps.Client(key=API_KEY)
# declaring locations 
locations = {
    "Antrim Area Hospital": "Antrim Area Hospital, Antrim, Northern Ireland",
    "Bellaghy":               "Bellaghy, Northern Ireland",
    "Coagh":                  "Coagh, Northern Ireland",
    "Draperstown":            "Draperstown, Northern Ireland",
    "Cookstown":              "Cookstown, Northern Ireland",
    "Maghera":                "Maghera, Northern Ireland",
    "Magherafelt":            "Magherafelt, Northern Ireland",
    "Randalstown":            "Randalstown, Northern Ireland",
    "Arboe":                  "Arboe, Northern Ireland",
}
#fetching distance matrixes 
print("fetching distance matrix...")
origins = list(locations.values())
destinations = list(locations.values())
matrix = gmaps.distance_matrix(origins,destinations, mode="driving", language="en-GB", units="imperial")


distances = {}
for i, origin in enumerate(origins):
    for j, destination in enumerate(destinations):
        info = matrix["rows"][i]["elements"][j]
        if info["status"] != "OK":
            print(f"Error fetching distance from {origin} to {destination}: {info['status']}")
            
        else:
            text  = info["distance"]["text"]
            miles = float(re.search(r"[\d\.]+", text) .group(0))

        from_name = list(locations.keys())[i]
        to_name = list(locations.keys())[j]
        distances[(from_name, to_name)] = miles
current = "Antrim Area Hospital"
log = []
total = 0.0 
print("starting at " + current)
print("enter next locattion as one of the following: " + ", ".join(locations.keys()))
print("type 'DONE' to quit")

while True:
    nxt = input(f"Next destination (from {current}): ").strip()
    if nxt.upper() == "DONE":
        break
    if nxt not in locations:
        print("  → Unknown place. Please choose from the list.")
        continue
    miles = distances.get((current, nxt))
    if miles is None:
        print(f"  → No route found {current} → {nxt}. Skipping.")
    else:
        log.append((current, nxt, miles))
        total += miles
        print(f"  → Logged {current} → {nxt}: {miles:.1f} mi (Total so far: {total:.1f} mi)")
        current = nxt

if current != "Antrim Area Hospital":
    ret = distances.get((current, "Antrim Area Hospital"))
    if ret:
        log.append((current, "Antrim Area Hospital", ret))
        total += ret
        print(f"\nReturning leg: {current} → Antrim Area Hospital: {ret:.1f} mi")

print("\n—— Today’s Trip Summary ——")
for o, d, m in log:
    print(f"{o} → {d}: {m:.1f} mi")
print(f"Total mileage: {total:.1f} miles")

