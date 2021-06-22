---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Roshambo Code Scramle
blurb: A fun little exercise to brush up on your HTML and JavaScript skills.
canonical: https://www.mcnz.com/2020/02/09/roshambo-code-scramble-game.html
---

Oh no! I dropped my laptop on the ground and the Roshambo course code spilled out all over the floor! (Fortunately, the <a href="https://www.mcnz.com/course/numberguesser.html">number guesser</a> is fine.)

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

<img src="https://images-na.ssl-images-amazon.com/images/I/61QkvmvEdVL.png" alt="rock paper scissors" class="img-fluid"/>


Here's a GitHub page with the code in raw, unformatted text:

[Roshambo Code Scramble](https://raw.githubusercontent.com/jheguevara/java101/master/shared_stuff/02%20first%20scramble.txt)

It's better to copy from the raw, unformatted text. Copying the text below might give you some unwanted HTML characters. YMMV.

<hr/>

if (clientGesture=='scissors') {

<pre>//server always chooses rock

&lt;div id="results"&gt;&lt;/div&gt;

result = "tie";

&lt;br/&gt;

&lt;script&gt;

&lt;a href="#" onclick="playRoshambo('paper')"&gt;paper&lt;/a&gt;

&lt;/body&gt;

Which one will it be?&lt;br/&gt;

&lt;/script&gt;

result = "win";

&lt;html&gt;

result = "lose";

&lt;a href="#" onclick="playRoshambo('rock')"&gt;rock&lt;/a&gt;

if (clientGesture=='rock') {

&lt;head&gt;

if (clientGesture=='paper') {

&lt;/html&gt;

playRoshambo = function(clientGesture){

&lt;/head&gt;

document.getElementById('results').innerHTML = result;

&lt;body&gt;

&lt;a href="#" onclick="playRoshambo('scissors')"&gt;scissors&lt;/a&gt;
</pre>

<hr/>

## Ajax Integration

If you're really clever, you'll integrate the following code into your script. But this challenge is only for those with the very biggest of brains.

Again, the [raw code is here](https://raw.githubusercontent.com/cameronmcnz/cameronmcnz/main/ajax-javascript.txt).

If you copy and paste the code below, you may pull in unwanted HTML characters from the webpage. Copying the raw code is the safest bet.

<hr/>
<pre>Here are the number of wins:
&lt;div id="wins"&gt;&lt;/div&gt;


&lt;script&gt;
let url = "http://100.24.244.253:8080/increasewins";
let ajaxRequest = new XMLHttpRequest();

ajaxRequest.onreadystatechange = function() {
    if (this.readyState == 4 &amp;&amp; this.status == 200) {
		console.log(this.responseText);
        let score = JSON.parse(this.responseText);
        document.getElementById("wins").innerHTML = score.wins;
    }
};
ajaxRequest.open("GET", url, true);
ajaxRequest.send();

&lt;/script&gt;</pre>

<hr/>

<h3>One Step Further</h3>

The script above hits a RESTful web service, deployed as a microservice to a Kubernetes cluster on Amazon. If you're really bold, you could code it on your own. Here's the GitHub repo for reference:

<a href="https://github.com/cameronmcnz/keeping-score/tree/main/src/main/java/com/mcnz/rps/rest">GitHub Keeping Score Code Repository</a>

<iframe width="560" height="315" src="https://www.youtube.com/embed/PSnGYWAVfJ0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<hr/>

<h3>One Step Backwards</h3>

This Single Page Interface (<a href="https://www.mcnz.com/course/rock-paper-scissors-unscrambled.html">SPI</a>) approach is a far cry from how we developed web applications in the days of Servlets and JSPs. Here's a version of the game that takes a more traditional, monolithic approach to implementation:

* <a href="http://rps-env.eba-uwjfetjg.us-east-1.elasticbeanstalk.com/index.jsp">Monolithic Rock-Paper-Scissors Game</a>
* <a href="https://github.com/cameronmcnz/rock-paper-scissors/tree/monolith/src/com/mcnz/rps/moai">Monolithic RPS Source Code</a>


Play the game. Check out the code!
