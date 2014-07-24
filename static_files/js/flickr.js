var GetFlickrUrl = function(photo) {
  return 'https://farm' + photo.farm +
         '.staticflickr.com/' + photo.server +
         '/' + photo.id + '_' + photo.secret + '.jpg';
}

var AddPhoto = function(photo) {
  $("#photos").append("<li><img src=\"" + GetFlickrUrl(photo) + "\"></li>");
};

var AddAllPhotos = function(photos) {
  for (i in photos) {
    AddPhoto(photos[i]);
  }
};

var DisplayPhotos = function(flickrPhotos) {
   AddAllPhotos(flickrPhotos.photos.photo);
};

var GetResults = function() {
  console.log("Hey!");
  var flickr = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=764a4955d5ea19e5e7ca0b4a8f9603a7&text=fractals&format=json&per_page=1&jsoncallback=?";
  var params = { "tags": $("#searchbox").val()};
  $("body").css( "background-image", "url(" + "https://farm3.staticflickr.com/2918/14719770844_436b32d57b.jpg" + ")" );
  $.getJSON(flickr, params, DisplayPhotos);
};

var Main = function() {
  GetResults();
}

$(document).ready(Main); 
  
