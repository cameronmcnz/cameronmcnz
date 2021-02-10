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

It's better to copy from the raw, unformatted text. Copying the text below might give you some unwanted HTML characters. YMMV.

<hr/>

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

</hr>

## Ajax Integration

If you're really clever, you'll integrate the following code into your script. But this challenge is only for those with the very biggest of brains.

Again, the [raw code is here](https://raw.githubusercontent.com/cameronmcnz/cameronmcnz/main/ajax-javascript.txt).

If you copy and paste the code below, you may pull in unwanted HTML characters from the webpage.

<pre>

<p>Here are the number of wins: <div id=&quot;wins&quot;></div></p>

<p> <script> let url = &quot;http://100.24.244.253:8080/increasewins&quot;; let ajaxRequest = new XMLHttpRequest();</p>

<p>ajaxRequest.onreadystatechange = function() {  if (this.readyState == 4 &amp;&amp; this.status == 200) {  console.log(this.responseText);  let score = JSON.parse(this.responseText);  document.getElementById(&quot;wins&quot;).innerHTML = score.wins;  } }; ajaxRequest.open(&quot;GET&quot;, url, true); ajaxRequest.send();</p>

<p></script></p>

</pre>




