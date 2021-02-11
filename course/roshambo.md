
<html>

<body>
<a href="https://raw.githubusercontent.com/cameronmcnz/cameronmcnz/main/course/roshambo.md">source code</a><br/>

Which one will it be?<br/>

<a href="#" onclick="playRoshambo('paper')">paper</a>
<a href="#" onclick="playRoshambo('rock')">rock</a>
<a href="#" onclick="playRoshambo('scissors')">scissors</a><br/>

<div id="results"></div><br/>

<div id="wins"></div>
<div id="losses"></div>
<div id="ties"></div>

<script>

playRoshambo = function(clientGesture){

	if (clientGesture=='rock') {
		result = "tie";
		url = "http://100.24.244.253:8080/increaseties";
	}

	if (clientGesture=='paper') {
		result = "win";
		url = "http://100.24.244.253:8080/increasewins";
	}

	if (clientGesture=='scissors') {
		result = "lose";
		url = "http://100.24.244.253:8080/increaselosses";
	}
	
	document.getElementById('results').innerHTML = result;
	
	let ajaxRequest = new XMLHttpRequest();
	ajaxRequest.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			console.log(this.responseText);
			let score = JSON.parse(this.responseText);
			document.getElementById("wins").innerHTML = "Wins: " + score.wins;
			document.getElementById("losses").innerHTML = "Losses: " + score.losses;
			document.getElementById("ties").innerHTML = "Ties: " + score.ties;
		}
	};
	
	ajaxRequest.open("GET", url, true);
	ajaxRequest.send();

}
</script>

</body>
</html>






