<p>The NASA file</p>

<script>

var url = 'https://api.nasa.gov/planetary/apod?api_key=MIsbLEcJgADzrllRcudAGlF1oRhDl3YvwHm0GKTb';
var httpRequest; //declare here for good scope
if (window.XMLHttpRequest) { // Mozilla, Safari, IE7+ ...
  httpRequest = new XMLHttpRequest();
} else if (window.ActiveXObject) { // IE 6 and older
  httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
}
httpRequest.onreadystatechange = function() {
  if (httpRequest.readyState === XMLHttpRequest.DONE && httpRequest.status == 200) {
    returnedData = httpRequest.responseText;
    var data = JSON.parse(returnedData);
	alert(data.date);
    if (data.hasOwnProperty('results')) {
      var dates = data.results.map(function(result) {
        return result.date;
        });
      console.log('dates: ',dates);
	  alert(dates);
     }
  } else {
    // still not ready or error occurred
  }
};
httpRequest.open('GET', url, true);
httpRequest.send(null);

</script>
