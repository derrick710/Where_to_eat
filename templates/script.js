// Google Maps API script
function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: { lat: YOUR_DEFAULT_LATITUDE, lng: YOUR_DEFAULT_LONGITUDE } // Set your default map center here
    });


    markers.forEach(function (marker) {
        new google.maps.Marker({
            position: marker.position,
            map: map,
            title: marker.title
        });
    });
}
