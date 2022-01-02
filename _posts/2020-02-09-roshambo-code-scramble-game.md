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



<pre>
} // end if

} // end if

} // end if

} // end method

if (clientGesture=='scissors') {

&lt;title&gt;Rock Paper Roshambo in JavaScript &lt;/title&gt;

&lt;div id="results"&gt;&lt;/div&gt;

result = "tie";

&lt;br/&gt;

&lt;script&gt;

&lt;a href="#" onclick="playRoshambo('paper')"&gt;paper&lt;/a&gt;

&lt;/body&gt;

&lt;p&gt;Which one will it be?&lt;/p&gt;

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

## Part II: The Java App

Here is the second scramble. I'm not putting the code on this page as people will confuse it with the code above:

https://github.com/jheguevara/java101/blob/master/shared_stuff/03%20second%20scramble.txt

Can you create a standalone Java application from this code? Can you compile it and run it on the command line? In Eclipse? 

Could you turn it into a Spring Boot app???


