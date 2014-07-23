var photos = [https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=764a4955d5ea19e5e7ca0b4a8f9603a7&text=fractals&format=json&jsoncallback=?]


var GetFlickrUrl = function(photo) {
  return 'https://farm' + photo.farm +
         '.staticflickr.com/' + photo.server +
         '/' + photo.id + '_' + photo.secret + '.jpg';
}

var AddPhoto = function(photo) {
  $("#photos").append("<li>" + GetFlickrUrl(photo) + "</li>");
};

var AddAllPhotos = function(photos) {
  for (i in photos) {
    AddPhoto(photos[i]);
  }
};

var Main = function() {
  AddAllPhotos(photos);
}

var AddPhoto = function(photo) {
  $("#photos").append("<li><img src=\"" + GetFlickrUrl(photo) + "\"></li>");
};

var DisplayPhotos = function(flickrPhotos) {
   AddAllPhotos(flickrPhotos.photos.photo);
};

var Main = function() {
var flickr = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=764a4955d5ea19e5e7ca0b4a8f9603a7&format=json&jsoncallback=?";
var params = { "tags": "fractals" };
$.getJSON(flickr, params, DisplayPhotos);
}