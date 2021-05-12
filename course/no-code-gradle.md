---
layout: mcnz/hidden-post
author: Cameron McKenzie
title: Lab 4 - No Code Gradle
blurb: Here's the Gradle lab with code from GitHub
canonical: https://www.mcnz.com/course/no-code-gradle.html
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/rY-MrvpZ6xU" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

# Introduction to Gradle

Here's Lab 4 with a twist. Instead of writing your own code, why not pull it from GitHub, and then build it with Gradle, just like you would do if you were a DevOps engineer out in the field.

## Part 1-3

Create a folder under C:\workspace\labs\gradle and in that directory clone a GitHub repo:

wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject
$ git clone https://github.com/cameronmcnz/MyProject.git

You may need to then move into the MyProject directory

cd My*

### Compile Java Code with javac

From the MyProject directory, look at the BadJava.java file. Then compile it with the Java compiler:

wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject
$ javac BadJava.java

Then run the bytecode

$ java BadJava

### Gradle Tasks

See what Gradle tasks are available:

wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject
$ gradle tasks

Then tell Gradle that you're all about Java:

apply plugin: 'java'

Now run the tasks again and note the difference.

wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject
$ gradle tasks


### Compile with Gradle

Compile your code with Gradle:

wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject (part7)
$ gradle classes

Now clean up your workspace:

wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject (part7)
$ gradle clean

Now build a JAR file:

wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject (part7)
$ gradle build

And clean up again:

$ gradle clean

### Switch Branches

Add and commit your changes:

git add .
git commit -m "done for now"

Then switch branches:

git checkout part5

### Part 5

Update your gradle file according to the lab guide.

Commands to issue include:

gradle build
gradle -q run

### Switch branches

To switch branches, add and commit again. Then do the checkout:

git add .
git commit -m "done again"

git checkout part7

### Run Tests

Look at the code added under the test folders. Follow section 7 in the book and then run the test command. Note that it will fail.

gradle test

Fix the test files so the test will pass. Then run your tests again.

gradle test


That just about covers it!

<figure class="figure">
  <img src="https://miro.medium.com/max/700/1*E5JMRbW525OHTa1Op7dGGA.png" alt="Java Features" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">Gradle Lifecycle.</figcaption>
</figure>

<figure class="figure">
  <img src="https://pbs.twimg.com/media/C-KM9LfXkAAUFHP?format=jpg" alt="Java Features" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">Maven Cheat Sheet.</figcaption>
</figure>



