---
layout: mcnz/hidden-post
author: Cameron McKenzie
title: Roshambo Code Scramble
blurb: A fun little exercise to brush up on your HTML and JavaScript skills.
---

# Jenkins, Jenkins, Jenkins!

Why does Jenkins use blue spheres? ([My interview with Kohsuke Kawaguchi](https://www.theserverside.com/video/Jenkins-creator-explains-why-a-successful-build-job-is-blue))

## Quick Look at Plugins

I'd like to take a quick look at plugins. Very quick.

Two things you'll need for this exercise:

<pre>
<b>
https://github.com/cameronmcnz/rock-paper-scissors.git

clean install pmd:pmd checkstyle:checkstyle findbugs:findbugs
</b>
</pre>

## Install Warnings Next Generation Plugin

You can follow along, but just watching is fine too.

To follow along:

1. Start Jenkins (wasadmin/wasadmin on localhost:8080)
2. Click 'Manage Jenkins' on the left and look for 'Manage Plugins'
3. Look for the 'Warnings Next Generation' plugin. Make sure you click the <em>Avaliable<em> tab, as shown in the image below.
4. Click the Checkbox next to 'Warnings Next Generation' and then click the "Install without Restart"
    
Note: Because a few plugins are a bit stale, the install may initially fail, you'll need to restart, and then do the installation a second time.

<img src="https://itknowledgeexchange.techtarget.com/coffee-talk/files/2020/12/jenkins-warnings-plugin.jpg" class="img-fluid">

## To reboot Jenkins:

Click the start button on Windows in the lower left, and right-click on the command prompt and choose 'Run as Administrator'

<pre>
cd C:\Program Files (*
cd jenk*
jenkins stop
jenkins status
jenkins start
</pre>

## Create a build job

Create a freestyle build job named rock-paper-errors

Set the Git repository as: 
<pre>
https://github.com/cameronmcnz/rock-paper-scissors.git
</pre>

### Build Step

Add the foll0wing <strong>build step</strong> as:

<em>Invoke Top Level Maven Targets</em>
<pre>
clean install pmd:pmd checkstyle:checkstyle findbugs:findbugs
</pre>
#### POST Build Step

Add the <em>Record copmiler warnings and static analysis results<em> option as a post build step.
    
Click the 'Add Tool' option a few times to add PMD, Findbugs and Checkstyle.

Then run the build!

<img src="https://itknowledgeexchange.techtarget.com/coffee-talk/files/2020/12/Jenkins-Checkstyle-plugin.jpg" alt="Jenkins Findbugs"/>

There's a video that describes the process on [theserverside](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Jenkins-Warnings-Plugin-CheckStyle-FindBugs-PMD-Example-Tutorial).



## Pipeline Code

<pre>
<b>
node {
    stage('Checkout') {
        git url: 'C:\\Software\\repos\\SimpleGreeting.git'
    }
    
    
    stage ('User Acceptance Test') {
    
     def response = input message: 'Is this build good to go?',
      parameters: [choice(choices: 'Yes\nNo',
       description: '', name: 'Pass')]
     
     if (response=="Yes") {
      stage('Deploy') {
       bat 'gradle build -x test'
      } 
     }
    }
}
</b>
</pre>













# Revisiting Roshambo!

<hr/>
Run each of these locally if you want. Just copy the code into a file and save it with an .html extension on your desktop.
<br/>

<a href="https://raw.githubusercontent.com/cameronmcnz/cameronmcnz/main/course/roshambo.md">roshamboA.html</a>   ~~   <a href="https://raw.githubusercontent.com/cameronmcnz/cameronmcnz/main/course/rps.md">RoshamboB.html</a>
<br/><br/>

## Do you want to play a game?

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

<hr/><hr/>

# Your Own CI Server?

Do we know enough to create our own CI/CD server?

## Clone the repo

Open a Git BASH shell in the C:\Workspace\ folder.

Clone the rock-paper-gradle repo with the following command:

<pre>git clone https://github.com/learn-devops-fast/rps-gradle.git</pre>

Then build the project. You have to be in the C:\Workspace\rps-gradle folder to do it, as that's where the gradle.build file is:

<pre>
cd C:\Workspace\rps*
gradle build
</pre>


## Optional Main Class

You can manually run the Roshambo game by opening the BASH shell in the following folder and run a java command:

<pre>
C:\Workspace\rps-gradle\builds\libs\ java -cp roshambo-1.0.jar com.mcnz.rps.DesktopGame
</pre>

### Do it in Gradle?

The main class in the Roshambo jar is: 

<pre>mainClassName = "com.mcnz.rps.DesktopGame"</pre>

If you want to run the glass with Gradle, look up the labs how to configure this. You may need to add the appropriate 'apply' to reference it and run it. (page 36)


### Prepare for continuous deployment

Add this to your Gradle build. (This only works if you cloned the GitHub repo in the C:/Workspace folder.)

<pre>
task copyFile(type: Copy) {
	from file("C:/Workspace/rps-gradle/build/libs/roshambo-1.0.jar")
	into file("C:/Software/apache-tomcat-9.0.8/lib")
}
</pre>

#### Continuous deployment

Is this better than Jenkins?

<pre>
cd C:\Workspace\rps-gradle
git pull origin
gradle build
gradle copyFile
</pre>

Can you put that in a file named continuous-integration.bat?

You can run it in bash. Just be sure to add the ./ in front of the command:

$ ./continuous-integration.bat

Can you schedule the bat file to run every hour with Windows Task Scheduler? If so, why would anyone need Jenkins?

<hr/>
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

