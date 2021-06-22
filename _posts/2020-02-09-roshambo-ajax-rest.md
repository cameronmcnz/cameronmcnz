---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Roshambo Ajax Integration
blurb: Here we integrate a RESTful API into the Roshambo app
canonical: https://www.mcnz.com/2020/02/09/roshambo-ajax-rest.html
---

## Ajax Integration

If you're really clever, you'll integrate the following code into your script. But this challenge is only for those with the very biggest of brains.

Again, the [raw code is here](https://raw.githubusercontent.com/cameronmcnz/cameronmcnz/main/ajax-javascript.txt).

The RESTful web service URL may change from time to time, so check for the correct URL. Right now this should work:

http://keepingthescore-env.eba-cgup4jh6.us-east-1.elasticbeanstalk.com/score/

or

http://3.222.19.178/score

http://3.222.19.178/score/increasewins

### Port 8080?

Sometimes the service runs on port 8080:

http://3.222.19.178:8080/score

http://keepingthescore-env.eba-cgup4jh6.us-east-1.elasticbeanstalk.com:8080/score/


If you copy and paste the code below, with the correct URL, you may pull in unwanted HTML characters from the webpage. Copying the raw code is the safest bet.

Make sure you use the <b>correct URL!</b>

<hr/>
<pre>Here are the number of wins:
&lt;div id="wins"&gt;&lt;/div&gt;


&lt;script&gt;
let url = "http://3.222.19.178/score/increasewins";
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

<a href="https://github.com/cameronmcnz/spring-boot-examples/tree/master/simple-spring-rest-keeping-score/src/main/java/com/mcnz/rps/rest">GitHub Keeping Score Code Repository</a>

<iframe width="560" height="315" src="https://www.youtube.com/embed/PSnGYWAVfJ0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<hr/>

<h3>One Step Backwards</h3>

This Single Page Interface (<a href="https://www.mcnz.com/course/rock-paper-scissors-unscrambled.html">SPI</a>) approach is a far cry from how we developed web applications in the days of Servlets and JSPs. Here's a version of the game that takes a more traditional, monolithic approach to implementation:

* <a href="http://rps-env.eba-uwjfetjg.us-east-1.elasticbeanstalk.com/index.jsp">Monolithic Rock-Paper-Scissors Game</a>
* <a href="https://github.com/cameronmcnz/rock-paper-scissors/tree/monolith/src/com/mcnz/rps/moai">Monolithic RPS Source Code</a>


Play the game. Check out the code!
