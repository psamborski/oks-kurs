(function($){
  $(function(){

    $('textarea').characterCounter();

    const mymap = L.map('map-wrapper').setView([51.2196492, 22.695445], 15);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1Ijoic2FtYmVlZWsiLCJhIjoiY2pyMnFrejh3MG41bjQ4cW1yMzhlcjJmdiJ9.F6pj8NphkjbHzqVhMqu2Xw'
    }).addTo(mymap);
    const mainOffice = L.marker([51.2154213, 22.6927163]).addTo(mymap);
    const lessons = L.marker([51.221425, 22.6990666]).addTo(mymap);
    mainOffice.bindPopup('<div class="info-content"><h6>OSK Kurs (ul. Racławicka 32).</h6><p style="font-size: 1.2em;">Biuro OSK Kurs.</p></div>');
    lessons.bindPopup('<div class="info-content"><h6>I LO im. W. Broniewskiego<br>w Świdniku (ul. Okulickiego 13).</h6><p style="font-size: 1.2em;">Miejsce wykładów.</p></div>').openPopup();

  }); // end of document ready
})(jQuery); // end of jQuery name space