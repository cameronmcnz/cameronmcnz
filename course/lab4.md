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
