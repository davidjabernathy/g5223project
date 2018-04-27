	var circle_size = 20;

	var mouse_position = { lat: 40.1, lng: 40.1 };

	var features = filteredEdges.features;
	var selectedRoads = new Set();
	var roadLengths = {};
	var roadCoords = {};
	var roadNames = {}
	var roadsNamesSet = new Set();

	var cityCoords = {
		columbus: [39.9612, -82.9988],
		cleveland: [41.4993, -81.6944],
		atlanta: [33.7490, -84.3880],
		chicago: [41.8781, -87.6298],
		detroit: [42.3314, -83.0458],
		milwaukee: [43.0389, -87.9065]
	}
	filteredEdges = columbusFilteredModerate;

	var selectionChanged = function() {
		map.removeLayer(edges);

		filteredEdges = window[String(citySelect.value) + "Filtered" + String(speedSelect.value)];//columbusFilteredSlow;

		features = filteredEdges.features;
		edges = L.geoJSON(filteredEdges, {style: blueStyle});
		edges.addTo(map);
	}

	var citySelect = document.querySelector("#city");
	citySelect.value = "columbus";

	citySelect.addEventListener("change", function () {
		//map.setView(cityCoords[citySelect.value])
		map.setView(filterededges.features[0].geometry.coordinates[0])
		selectionChanged();
	})

	var speedSelect = document.querySelector("#speed");
	speedSelect.value = "Moderate";

	speedSelect.addEventListener("change", function () {
		selectionChanged();
	});

	function getMeterPerPixel() {
		var y = map.getSize().y;
		var x = map.getSize().x;

		var maxMeters = map.containerPointToLatLng([0,y]).distanceTo(map.containerPointToLatLng([x,y]));
		var MeterPerPixel = maxMeters/x;
		return MeterPerPixel;
	}

	var panView = function (lat, lng) {
	panorama = new google.maps.StreetViewPanorama(
			document.getElementById('street-view'),
			{
				position: {lat: lat, lng: lng},
				pov: {heading: 165, pitch: 0},
				zoom: 1
			});
	}


	function geocodeLatLng(geocoder, coords) {
		var latlng = {lat: coords[1], lng: coords[0]};
		//console.log(latlng)
		geocoder.geocode({'location': latlng}, function(results, status) {
			if (status === 'OK') {
				//console.log(results)
				if (results[0]) {
					result = results[0].address_components[1].long_name;
				}
			}
		});
		return result
	}

	var map = L.map('map', {drawControl: true}).setView([39.9612, -82.9988], 11.5);
	map.createPane('labels');
	map.getPane('labels').style.zIndex = 650;

  var edges = {"type": "LineString", "coordinates": [[40.1200793, -83.0364405], [40.120086, -83.036841], [40.120059, -83.037353], [40.120042, -83.037529], [40.120028, -83.038165], [40.120031, -83.038371]]};
  var edge1 = {"type": "LineString", "coordinates": [[-83.0364405, 40.1200793], [-83.036841, 40.120086], [-83.037353, 40.120059], [-83.037529, 40.120042], [-83.038165, 40.120028], [-83.038371, 40.120031]]};

  var redStyle = {
      "color": "#dbdde0",
      "weight": 1,
      "opacity": .6
  };

  var blueStyle = {
      "color": "#FFA500",
      "weight": 2,
      "opacity": .8
  };

	var latMin = 0;
	var latMax = 0;
	var lonMin = 0;
	var lonMax = 0;
  map.on('mousemove', function(e) {
        mouse_position = e.latlng;
				bounds = circle.getBounds();
				latMin = Math.abs(bounds.getSouth());
				latMax = Math.abs(bounds.getNorth());
				lonMin = Math.abs(bounds.getEast());
				lonMax = Math.abs(bounds.getWest());
		circle.setLatLng(mouse_position);
    });

  map.on('zoomend', function(e) {
  circle.setRadius(circle_size * self.getMeterPerPixel());
  });

  var edges = L.geoJSON(filteredEdges, {style: blueStyle});
	edges.addTo(map);


	L.tileLayer('https://api.mapbox.com/styles/v1/amasw87/cjg5on93k0eal2sp6wres4x0p/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYW1hc3c4NyIsImEiOiJjajZ6aG50bnUwMGpqMnBvOGJjNTk0cHFvIn0.IXHyLgImAw0H_dlCs7ZEgA', {
		maxZoom: 15,
	}).addTo(map);

	var labelLink = 'https://api.mapbox.com/styles/v1/amasw87/cjgcjnead0wog2rmwpbai4hjk/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiYW1hc3c4NyIsImEiOiJjajZ6aG50bnUwMGpqMnBvOGJjNTk0cHFvIn0.IXHyLgImAw0H_dlCs7ZEgA';
	L.tileLayer(labelLink, {
			maxZoom: 13,
			pane: 'labels'
		}).addTo(map);
		var circle = L.circle([39.9612, -82.9988], {
				color: '#f03',
				opacity: 0,
				fillColor: '#0066ff',
				fillOpacity: 0.4,
				radius: circle_size * self.getMeterPerPixel()
		});
		circle.addTo(map);

map.on('click', function(e) {

	//console.log(e.latlng)
	selectedRoads.clear();
	roadsNamesSet.clear();
	roadLengths = {};
	document.querySelector("#streetText").innerHTML = "";
	for(var i = 0; i < features.length; i++) {
		//console.log(features.length)
		var coords = features[i].geometry.coordinates
		for(var j = 0; j < coords.length; j++) {
			var lat  = Math.abs(coords[j][1]);
			var lon = Math.abs(coords[j][0]);
			if(lat > latMin && lat < latMax && lon > lonMin && lon < lonMax) {
				var roadLength = features[i].properties.length;
				var roadCoord = features[i].geometry.coordinates[0];
				var name = features[i].properties.name;
				var id = features[i].id;
				if(typeof(name) != "string") {
					var geocoder = new google.maps.Geocoder;
					name = geocodeLatLng(geocoder, roadCoord);

				}
				if(!selectedRoads.has(id) && !roadsNamesSet.has(name)) {
					selectedRoads.add(id)
					roadsNamesSet.add(name);
					roadLengths[id] = roadLength;
					roadCoords[id] = roadCoord;
					roadNames[id] = name;
					value = id;
					document.querySelector("#streetText").innerHTML += "<p><span class=\"button\" id=\"" +id + "\">" + roadNames[value] + "</span><br>" + roadLengths[value] + "<br>" + roadCoords[value] +"<br><br></p>";
				}


			}
		}

	}

	selectedRoads.forEach(function(value, key, setObj) {


		//document.querySelector("#sideInfo").innerHTML = '<iframe src="https://maps.googleapis.com/maps/api/streetview?size=600x300&location=46.414382,10.013988&heading=151.78&pitch=-0.76&key=AIzaSyD65f4ivv0_b8Rhq7GMN-oaFx12MtpN1No"></iframe>'


	})
	var btns = document.querySelectorAll(".button")
	for(var b = 0; b < btns.length; b++) {
		btns[b].addEventListener("click", function() {
			//console.log(roadCoords[this.id])

			panView(roadCoords[this.id][1], roadCoords[this.id][0])
			// console.log(roadCoords[this.textContent])
		})
	}

	//panView(40.0092335, -83.0123744)


	//document.querySelector("#sideInfo").textContent = name;
	//https://www.google.com/maps/embed/v1/place?key=AIzaSyAgGQRYnWTzsgf6Xn1DISE99Tdq7Lr9rwU&q=Eiffel+Tower,Paris+France
})
