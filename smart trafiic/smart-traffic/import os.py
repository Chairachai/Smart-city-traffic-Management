import os
import zipfile

# Folder structure and files
files = {
    "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Smart Traffic Management</title>
  <link rel="stylesheet" href="css/style.css">
  <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY"></script>
  <script src="js/map.js" defer></script>
  <script src="js/simulation.js" defer></script>
</head>
<body>
  <h1>Smart Traffic Map - Bengaluru</h1>
  <div id="map" style="width:100%;height:600px;"></div>
  <button onclick="refreshTraffic()">Refresh Traffic Data</button>
</body>
</html>""",
    "css/style.css": """body { font-family: Arial, sans-serif; margin: 0; padding: 0; }""",
    "js/map.js": """let map; let markers = [];
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 12.9716, lng: 77.5946 }, zoom: 12
    });
    fetch('data/hotspots.json')
        .then(response => response.json())
        .then(data => {
            data.forEach(loc => {
                let color = loc.traffic === "high" ? "red" : loc.traffic === "medium" ? "orange" : "green";
                let marker = new google.maps.Marker({
                    position: {lat: loc.lat, lng: loc.lng},
                    map: map,
                    title: loc.name,
                    icon: { path: google.maps.SymbolPath.CIRCLE, scale: 10, fillColor: color, fillOpacity: 0.8, strokeWeight: 1 }
                });
                markers.push(marker);
            });
        });
}
window.initMap = initMap;""",
    "js/simulation.js": """function refreshTraffic() {
    markers.forEach(marker => {
        let trafficLevel = ["low","medium","high"][Math.floor(Math.random()*3)];
        let color = trafficLevel === "high" ? "red" : trafficLevel === "medium" ? "orange" : "green";
        marker.setIcon({ path: google.maps.SymbolPath.CIRCLE, scale: 10, fillColor: color, fillOpacity: 0.8, strokeWeight: 1 });
    });
}
setInterval(refreshTraffic, 5000);""",
    "js/charts.js": """// Add Chart.js in dashboard.html for charts""",
    "data/hotspots.json": """[
  {"name": "Silk Board Junction", "lat": 12.9178, "lng": 77.6225, "traffic": "high"},
  {"name": "Tin Factory Junction", "lat": 13.0256, "lng": 77.6586, "traffic": "medium"},
  {"name": "Marathahalli", "lat": 12.9499, "lng": 77.7013, "traffic": "high"}
]""",
    "README.md": """# Smart Traffic Management Demo
Open index.html in browser with internet. Refresh button simulates traffic updates."""
}

# Create directories
os.makedirs("smart-traffic/css", exist_ok=True)
os.makedirs("smart-traffic/js", exist_ok=True)
os.makedirs("smart-traffic/data", exist_ok=True)

# Write files
for path, content in files.items():
    with open(os.path.join("smart-traffic", path), "w") as f:
        f.write(content)

# Create zip
with zipfile.ZipFile("smart-traffic.zip", "w") as zipf:
    for foldername, subfolders, filenames in os.walk("smart-traffic"):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            zipf.write(filepath, os.path.relpath(filepath, "smart-traffic"))

print("smart-traffic.zip created successfully!")
