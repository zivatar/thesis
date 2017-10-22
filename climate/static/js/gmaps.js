var marker;

function setLatLon() { /* only placeholder */ }

function GMselectOneStation() {
  var mapCanvas = document.getElementById("google_maps_one_marker");

  var positions = getPos();
  
  console.log(positions[0]);
  var mapOptions = {
    center: new google.maps.LatLng(positions[0].position),
    zoom: 8,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  }
  var map = new google.maps.Map(mapCanvas, mapOptions);

    var pos = positions[0];
    pos.map = map;
    new google.maps.Marker(pos);

  google.maps.event.addListener(map,'click',function(event) {
  	var location = event.latLng;
  	if(!marker) { marker = new google.maps.Marker({ position: location, map: map }); }
  	else {marker.setPosition(location)}
  	//document.getElementById("lat").value = location.lat();
  	//document.getElementById("lon").value = location.lng();
	setLatLon(location.lat(), location.lng());
  });
}

function getPos() { /* only placeholder	*/ }

function GMallStations() {
	var positions = getPos();
	var mapCanvas = document.getElementById("google_maps_all_stations");
	var mapOptions = { mapTypeId: google.maps.MapTypeId.TERRAIN, maxZoom: 14, };
	var map = new google.maps.Map(mapCanvas, mapOptions);
	var bounds = new google.maps.LatLngBounds();
  
	for ( var i = 0; i < positions.length; i++ ) {
		var pos = positions[i];
		pos.map = map;
		new google.maps.Marker(pos);
		bounds.extend(pos.position);
	}

	map.fitBounds(bounds);
}

function GMoneStation() {
  var positions = getPos();
  var mapCanvas = document.getElementById("google_maps_one_station");
  var mapOptions = { mapTypeId: google.maps.MapTypeId.TERRAIN, maxZoom: 14, };
  var map = new google.maps.Map(mapCanvas, mapOptions);
  var bounds = new google.maps.LatLngBounds();
  
  for ( var i = 0; i < positions.length; i++ ) {
    var pos = positions[i];
    pos.map = map;
    new google.maps.Marker(pos);
    bounds.extend(pos.position);
  }

  map.fitBounds(bounds);
}
