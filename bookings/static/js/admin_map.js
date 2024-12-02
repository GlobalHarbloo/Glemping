var $j = jQuery.noConflict();

$j(document).ready(function() {
    var latitude = parseFloat($j('#id_marker_latitude').val()) || 0.0;
    var longitude = parseFloat($j('#id_marker_longitude').val()) || 0.0;

    var mapContainer = $j('#map-container');
    var marker = $j('#marker');

    updateMarkerPosition(latitude, longitude);

    function updateMarkerPosition(lat, lng) {
        marker.css({
            left: (lng * 100) + '%',
            top: (lat * 100) + '%',
        });
    }

    mapContainer.click(function(e) {
        var offset = mapContainer.offset();
        var width = mapContainer.width();
        var height = mapContainer.height();

        var lat = (e.pageY - offset.top) / height;
        var lng = (e.pageX - offset.left) / width;

        updateMarkerPosition(lat, lng);

        $j('#id_marker_latitude').val(lat);
        $j('#id_marker_longitude').val(lng);
    });
});
