var GetFlickrUrl = function(photo) {
  return 'https://farm' + photo.farm + '.staticflickr.com/' + photo.server + '/' + photo.id + '_' + photo.secret + '.jpg';
};

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
  console.log("Let's search for bugs or know how our page works!");
  var flickr = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=764a4955d5ea19e5e7ca0b4a8f9603a7&text=fractals&format=json&per_page=1&jsoncallback=?";
  var params = { "tags": "fractals" };
  $("body").css( "background-image", "url(" + GetFlickrUrl + ")" );
  $.getJSON(flickr, params, DisplayPhotos);
};

var Main = function() {
  GetResults();
};

$(document).ready(Main); 