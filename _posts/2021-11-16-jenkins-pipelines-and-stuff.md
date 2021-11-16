---
layout: mcnz/basic-post
author: Cameron McKenzie
title: wa 2917 Day 5 Jenkins Pipelines
blurb: Here we'll look at Jenkins pipelines
canonical: https://www.mcnz.com/2021/11/16/jenkins-pipelines-and-stuff.html
---
<iframe width="560" height="315" src="https://www.youtube.com/embed/ei7kv7QOMC8" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Today's Agenda
--------------

We have three Jenkins labs on the docket:

1. Jenkins Build Jobs
2. Create a pipeline (Lab 6) (https://www.youtube.com/watch?v=ei7kv7QOMC8)
3. Advanced Pipelines with Groovy (Lab 7 - May give time Thursday) (https://www.youtube.com/watch?v=5oinW9bN2DI)

Lab Confusion
-------------

The advanced pipeline lab has some code that should go all on one line, but spans two lines in the book for formatting reasons. Be careful. This trips up a lot of students.

<figure class="figure">
  <img src='/images/groovy-image.png' alt="Microservices Monoliths pooh" class="img-fluid mx-auto d-block img-thumbnail rounded " >
  <figcaption class="figure-caption">The pooh emoji Monolith vs microservices architecture diagram.</figcaption>
</figure>

We did a Jenkins build job example together last week. Today we will talk about Jenkins more formally.

We will cover sections 6 and 7 in the book today:

- Chapter 6 Jenkins Jobs
- Chapter 7 Jenkins Pipelines

Jenkins Job Example
-------------------

Want a cool example of how Jenkins and Plugins really raise the game? 

Install the Warnings Next Generation Plugin and use these parameters in a new Jenkins job:

- git clone https://github.com/cameronmcnz/spock-lizard-docker.git
- mvn install checkstyle:checkstyle findbugs:findbugs pmd:pmd

Then add the warnings plugin to the post build steps. 

View this link for more details:

https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Jenkins-Warnings-Plugin-CheckStyle-FindBugs-PMD-Example-Tutorial

Pipeline Examples
-----------------

To really drive home how pipelines work, I'd like to review these two pipeline examples together (Time permitting)

1. https://github.com/cameronmcnz/rock-paper-scissors/blob/master/scripted-pipeline
2. https://github.com/cameronmcnz/spock-lizard-docker/blob/master/Jenkinsfile

The remainder of the day after that will be yours to complete the labs and the homework assignments.


