---
layout: mcnz/basic-post
author: Cameron McKenzie
title: GitFlow, Branch Merging, Maven and Java Builds
blurb: Here's how to merge GitFlow branches and build your Java apps with Maven.
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/d4cDLBFbekw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

# Git Flow and Maven Tutorial

You are the team lead on an important project, and your developers have all told you their feature branches are complete, but they've all gone home for the weekend, and you want to build a release.

Currently, the GitFlow diagram looks like this:

<a href="https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/GitFlow-Hotfix-Branch-Example-Start-Finish">
<img src="https://itknowledgeexchange.techtarget.com/coffee-talk/files/2021/01/gitflow-release-branch.jpg" alt="gitflow before merges" class="img-fluid mx-auto d-block">
</a>

The process of merging branches, building the app, running tests, creating a release branch and then testing your application before it merges into main will require the following commands:

<pre>

git clone https://github.com/cameronmcnz/learn-devops
git branch -a

git checkout <branchname>
git merge <branchname>

mvn clean
mvn compile
mvn test
mvn clean install tomcat7:exec-war-only

java -jar executable.jar


</pre>
## Clone the Remote Repository

Create a folder named C:\workspace and open this folder up in the BASH shell. This can be done by right-clicking on the folder in Windows Explorer and selecting Git Bash Here.

Issue the following command to clone the repository:
<pre>
git clone https://github.com/cameronmcnz/learn-devops
</pre>

A new folder will appear in C:\workspace named learn-devops. This folder will contain another folder named numberguesser. Open the C:\workstation\learn-devops\numberguesser folder in Windows Explorer and note the existence of a POM file. This file indicates that the numberguesser is a Maven based project.

Right click on the numberguesser folder and select Git Bash Here to open a terminal window in this folder.

Type the ls command into the terminal window to ensure the POM file is in the BASH windows's directory.
<pre>
me@computer MINGW64 /c/workspace/learn-devops/numberguesser (main)
$ ls
pom.xml  src/
</pre>




<figure class="figure">
  <img src="https://itknowledgeexchange.techtarget.com/coffee-talk/files/2021/01/gitflow-hotfix-branch-diagram.jpg" alt="Git flow init branches" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">The git flow init command preps your workspace for main, master, feature, release and hotfix branch creations.</figcaption>
</figure>


