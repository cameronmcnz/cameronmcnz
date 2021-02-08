---
layout: mcnz/hidden-post
author: Cameron McKenzie
title: Fun with Gradle
blurb: Take your Gradle and Groofy to the next level
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/tK7gd9Q0lBE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

# Clone the repo

Clone the rock-paper-gradle repo with the following command:

<pre>git clone https://github.com/learn-devops-fast/rps-gradle.git</pre>

Now run the main class.


## Main Class

The main class in the Roshambo jar is: 

<pre>mainClassName = "com.mcnz.rps.DesktopGame"</pre>

You may need to add the appropriate 'apply' to reference it and run it.

### Prepare for continuous deployment

Add this to your Gradle build

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

Can you schedule it to run every hour with Windows Task Scheduler? If so, why would anyone need Jenkins?
