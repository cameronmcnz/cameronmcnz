---
layout: mcnz/hidden-post
author: Cameron McKenzie
title: Roshambo Code Scramble
blurb: A fun little exercise to brush up on your HTML and JavaScript skills.
---
# Spring Development

You can find the code for this example on GitHub:

https://github.com/learn-devops-fast/lab-4-spring-boot

Here are the individual files we will be building:

## build.gradle

https://raw.githubusercontent.com/learn-devops-fast/lab-4-spring-boot/main/build.gradle

## HelloApi.Java

https://github.com/learn-devops-fast/lab-4-spring-boot/blob/main/src/main/java/com/webage/spring/samples/hello/HelloApi.java

## HelloResponse

https://raw.githubusercontent.com/learn-devops-fast/lab-4-spring-boot/main/src/main/java/com/webage/spring/samples/hello/api/HelloResponse.java

## HelloResource

https://raw.githubusercontent.com/learn-devops-fast/lab-4-spring-boot/main/src/main/java/com/webage/spring/samples/hello/api/HelloResource.java

## Score

https://raw.githubusercontent.com/learn-devops-fast/lab-4-spring-boot/main/src/main/java/com/mcnz/roshambo/Score.java

## ScoreService

https://raw.githubusercontent.com/learn-devops-fast/lab-4-spring-boot/main/src/main/java/com/mcnz/roshambo/ScoreService.java




The link to this page is: http://www.mcnz.com/course/

# Code Scramble!

Oh no! I dropped my laptop on the ground and the course code spilled out all over the floor!

I threw all the lines of code back into a text file, but none of the lines are in order.

Plus, a bunch of end brackets fell down a sewer grate, so I need your help finding a few.

## Instructions

Use editpad or notepad and rearrange [the code](https://raw.githubusercontent.com/jheguevara/java101/master/shared_stuff/02%20first%20scramble.txt) so that it will run a little rock-paper-scissors application in your web browser.
<hr/>

[The Scrambled Code](https://raw.githubusercontent.com/jheguevara/java101/master/shared_stuff/02%20first%20scramble.txt)
<hr/>

Here are some tips:

* Use each line of code once and only once.
* Do not write any of your own code. (An end curly bracket or two is okay)
* Group similar looking pieces of code together as you are starting out.
* Do not write any of your own code. (An end curly bracket or two is okay)
* Group HTML tag elements together and elements that look like code together
* Do not write any of your own code. (An end curly bracket or two is okay)
* When you think your done, save the file as rps.html and open it in a web browser and see if it works!!!
* Do not write any of your own code. (An end curly bracket or two is okay)

<img src="https://images-na.ssl-images-amazon.com/images/I/61QkvmvEdVL.png" alt="rock paper scissors" class="img-fluid"/>

### The Scrambled Code

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

<img src="https://upload.wikimedia.org/wikipedia/commons/f/f1/Pilot_seen_running_to_fighter.jpg" alt="scramble for jets" class="img-fluid"/>

