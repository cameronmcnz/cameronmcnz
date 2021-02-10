---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Roshambo Code Scramle
blurb: A fun little exercise to brush up on your HTML and JavaScript skills.
---

Oh no! I dropped my laptop on the ground and the course code spilled out all over the floor!

I threw all the lines of code back into a text file, but none of the lines are in order.

Plus, a bunch of end brackets fell down a sewer grate, so I need your help finding a few.

## Instructions

Use editpad or notepad and rearrange the code so that it will run a little rock-paper-scissors application in your web browser.

Here are some tips:

* Use each line of code once and only once.
* Do not write any of your own code.
* Group similar looking pieces of code together as you are starting out.
* Do not write any of your own code.
* Group HTML tag elements together and elements that look like code together
* Do not write any of your own code.
* When you think your done, save the file as rps.html and open it in a web browser and see if it works!!!

Here's a GitHub page with the code in raw, unformatted text:

[Roshambo Code Scramble](https://raw.githubusercontent.com/jheguevara/java101/master/shared_stuff/02%20first%20scramble.txt)

<pre>

//server always chooses rock

<div id="results"></div>

result = "tie";

<br/>

<script>

<a href="#" onclick="playRoshambo('paper')">paper</a>

</body>

Which one will it be?<br/>

</script>

result = "win";

<html>

result = "lose";

<a href="#" onclick="playRoshambo('rock')">rock</a>

if (clientGesture=='rock') {

<head>

if (clientGesture=='paper') {

</html>

playRoshambo = function(clientGesture){

</head>

document.getElementById('results').innerHTML = result;

<body>

<a href="#" onclick="playRoshambo('scissors')">scissors</a>

if (clientGesture=='scissors') {
</pre>


## Ajax Integration

If you're really clever, you'll integrate the following code into your script. But this challenge is only for those with the very biggest of brains.

<pre>

Here are the number of wins:
<div id="wins"></div>


<script>
let url = "http://100.24.244.253:8080/increasewins";
let ajaxRequest = new XMLHttpRequest();

ajaxRequest.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
		console.log(this.responseText);
        let score = JSON.parse(this.responseText);
        document.getElementById("wins").innerHTML = score.wins;
    }
};
ajaxRequest.open("GET", url, true);
ajaxRequest.send();

</script>

</pre>




