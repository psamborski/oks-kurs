(function($){
  $(function(){

    $('textarea').characterCounter();

    var mymap = L.map('map-wrapper').setView([51.505, -0.09], 13);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic2FtYmVlZWsiLCJhIjoiY2pyMnFrejh3MG41bjQ4cW1yMzhlcjJmdiJ9.F6pj8NphkjbHzqVhMqu2Xw', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'your.mapbox.access.token'
    }).addTo(mymap);
    // TODO fix maps
	
  }); // end of document ready
})(jQuery); // end of jQuery name space

// function initialize() {
//     var map;
//     var bounds = new google.maps.LatLngBounds();
//     var mapOptions = {
//         mapTypeId: 'roadmap'
//     };
//
//     // Display a map on the page
//     map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
//     map.setTilt(45);
//
//     // Multiple Markers
//     var markers = [
//         ['Racławicka 32, biuro OSK Kurs', 51.2154213,22.6927163],
//         ['I LO w Świdniku, Świdnik', 51.221425,22.6990666]
//     ];
//
//     // Info Window Content
//     var infoWindowContent = [
//         ['<div class="info-content">' +
//         '<h6>OSK Kurs (ul. Racławicka 32).</h6>' +
//         '<p>Biuro OSK Kurs.</p>' +        '</div>'],
//         ['<div class="info-content">' +
//         '<h6>I LO im. W. Broniewskiego<br>w Świdniku (ul. Okulickiego 13).</h6>' +
//         '<p>Miejsce wykładów.</p>' +
//         '</div>']
//     ];
//
//     // Display multiple markers on a map
//     var infoWindow = new google.maps.InfoWindow(), marker, i;
//
//     // Loop through our array of markers & place each one on the map
//     for( i = 0; i < markers.length; i++ ) {
//         var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
//         bounds.extend(position);
//         marker = new google.maps.Marker({
//             position: position,
//             map: map,
//             title: markers[i][0]
//         });
//
//         // Allow each marker to have an info window
//         google.maps.event.addListener(marker, 'click', (function(marker, i) {
//             return function() {
//                 infoWindow.setContent(infoWindowContent[i][0]);
//                 infoWindow.open(map, marker);
//             }
//         })(marker, i));
//
//         // Automatically center the map fitting all markers on the screen
//         map.fitBounds(bounds);
//     }
//
//     // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
//     var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
//         this.setZoom(14);
//         google.maps.event.removeListener(boundsListener);
//     });
// }