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

ls

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

Issue the following command to make sure all of the Java code compiles:
<pre>
mvn compile
</pre>
The command may report some errors, but there should be a green BUILD SUCCESS message indicating that the code compiled successfully.

Make sure all of the tests pass by issuing the following command:
<pre>
mvn test
</pre>

List all of the local and remote branches.

<pre>
$ git branch -a
* main
  remotes/origin/FEATURE/enhance_webpage
  remotes/origin/FEATURE/game_logic
  remotes/origin/FEATURE/negatives_fix
  remotes/origin/HEAD -> origin/main
  remotes/origin/development
  remotes/origin/main
</pre>

Check out the remote FEATURE/enhance_webpage branch to make it local.
<pre>
git checkout FEATURE/enhance_webpage
</pre>
List the branches to prove the checked out branch has become local:
<pre>
$ git branch -a
* FEATURE/enhance_webpage
  main
  remotes/origin/FEATURE/enhance_webpage
  remotes/origin/FEATURE/game_logic
  remotes/origin/FEATURE/negatives_fix
  remotes/origin/HEAD -> origin/main
  remotes/origin/development
  remotes/origin/main
</pre>

In Windows Explorer, open the \numberguesser\src\main\java\com\mcnz\servlet folder.

Note the number of Java files in this folder. We want to merge these files into the development branch.

Checkout the development branch with the following command:

git checkout development

There should now only be one Java file in the \servlet folder, whereas before there were two.

Merge the FEATURE/enhance_webpage branch into development
<pre>
git merge FEATURE/enhance_webpage
</pre>
After the merge, the 

Compile and Test

After the merge, compile and test the code on the development branch with the following two commands:
<pre>
mvn compile
mvn test
</pre>
## Merge the Game Logic Branch

Checkout the FEATURE/game_logic branch:
<pre>
git checkout FEATURE/game_logic
</pre>
Count the number of Java files in the \servlet folder monitored earlier. There should be 3 now.

Merge the FEATURE/game_logic branch into the development branch. First checkout the development branch. Then perform the merge.
<pre>
git checkout development
git merge FEATURE/game_logic
</pre>

Note the number of files in the development branch's \servlet folder has changed to match the FEATURE/game_logic branch.

Compile the merged code and test it.

<pre>
mvn compile
mvn test
</pre>

Now merge the remotes/origin/FEATURE/negatives_fix branch.

A checkout of the FEATURE/negatives_fix branch is required to make the remote branch local.

<pre>
git checkout FEATURE/negatives_fix
</pre>

Return to the development branch. Merge, compile and test the code. 

The compile and test still will initially fail.

<pre>
git checkout development
git merge FEATURE/game_logic
</pre>

There is a compilation error in the merged code, so the compile command will fail:

<pre>
mvn compile
[ERROR] numberguesser/src/main/java/com/mcnz/servlet/CoreLogic.java:[26,68] ';' expected
<pre>




</pre>




<figure class="figure">
  <img src="https://itknowledgeexchange.techtarget.com/coffee-talk/files/2021/01/gitflow-hotfix-branch-diagram.jpg" alt="Git flow init branches" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">The git flow init command preps your workspace for main, master, feature, release and hotfix branch creations.</figcaption>
</figure>


