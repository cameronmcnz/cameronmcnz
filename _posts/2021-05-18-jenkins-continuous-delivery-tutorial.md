---
layout: mcnz/hidden-post
author: Cameron McKenzie
title: Jenkins Continuous Delivery Example
blurb: "This quick Jenkins tutorial give an example of how to implement continuous delivery with the popular JenkinsCI CI/CD tool."
canonical: https://www.mcnz.com/2021/05/18/jenkins-continuous-delivery-tutorial.html
---

# Continuous Delivery with Jenkins CI

<iframe width="560" height="315" src="https://www.youtube.com/embed/Mas5HjFHwvo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Continuous delivery jobs with Jenkins

Make sure Jenkins is started, and no other programs, such as an app running in the SpringSource Tool Suite, or a running Java JAR file, is blocking port 8080.

The Jenkins URL is: http://localhost:8080

## Spring Boot Jenkins Builds

Here's a quick example of how to do continuous delivery with Jenkins. In this example, we not only build a Spring Boot app with Maven, but we run the JAR file that gets created and we test the JSON returned from a web based invocation.

Here is the GitHub repository used in the example:

https://github.com/cameronmcnz/rps-maven

The Maven command used is:

<pre><code>clean compile package</code></pre>

The code used in the second build step is available here:

https://raw.githubusercontent.com/cameronmcnz/rps-maven/main/website-status-check.txt

Ever wonder why does Jenkins uses blue spheres? ([My interview with Kohsuke Kawaguchi](https://www.theserverside.com/video/Jenkins-creator-explains-why-a-successful-build-job-is-blue))


<iframe width="560" height="315" src="https://www.youtube.com/embed/BiIuR4aQK9A" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

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








<img src="https://upload.wikimedia.org/wikipedia/commons/f/f1/Pilot_seen_running_to_fighter.jpg" alt="scramble for jets" class="img-fluid"/>

