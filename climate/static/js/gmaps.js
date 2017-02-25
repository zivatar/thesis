var marker;

function GMselectOneStation() {
  var mapCanvas = document.getElementById("google_maps_one_marker");
  var mapOptions = {
    center: new google.maps.LatLng(47.6, 19.0),
    zoom: 8,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  }
  var map = new google.maps.Map(mapCanvas, mapOptions);

  google.maps.event.addListener(map,'click',function(event) {
  	var location = event.latLng;
  	if(!marker) { marker = new google.maps.Marker({ position: location, map: map }); }
  	else {marker.setPosition(location)}
  	document.getElementById("lat").value = location.lat();
  	document.getElementById("lon").value = location.lng();
  });
}

function GMallStations() {
  var mapCanvas = document.getElementById("google_maps_all_stations");
  
  var mapOptions = {
    mapTypeId: google.maps.MapTypeId.TERRAIN
  }
  var map = new google.maps.Map(mapCanvas, mapOptions);
  var pos1 = { position: {lat: 47.5, lng: 19.0}, title: 'egyik', map: map };
  var pos2 = { position: {lat: 47.4, lng: 18.9}, title: 'masik', map: map };
  marker2 = new google.maps.Marker(pos1);
  marker2 = new google.maps.Marker(pos2);
	var bounds = new google.maps.LatLngBounds();
	bounds.extend(pos1.position);
	bounds.extend(pos2.position);
	map.fitBounds(bounds);
}