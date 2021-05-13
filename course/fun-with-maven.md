---
layout: mcnz/hidden-post
author: Cameron McKenzie
title: "Here's some fun with Maven"
blurb: "Let's contrast Maven against Gradle"
canonical: https://www.mcnz.com/course/fun-with-maven.html
---
<style>
pre code {
  background-color: #eee;
  border: 1px solid #999;
  display: block;
  padding: 20px;
}
</style>

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/VHz5gs5ANGE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

# Introduction to Maven

We may run an application on port 8080 in this exercise, so make sure the Jenkins service is stopped. (3:45 in the YouTube video)

Here's a compliment to Lab 4. While Gradle is the new kid on the block, the majority of enterprise Java projects in production today use Maven.

My apologies, but this is just going to be a lot of code snippets for you to type.

## Clone from GitHub

Create a folder under C:\workspace\labs\ named maven and in that directory clone the rps-maven GitHub repo:

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/maven
$ git clone https://github.com/cameronmcnz/rps-maven.git
</code></pre>
You may need to then move into the MyProject directory

<pre><code>cd rps*</code></pre>

#### Compile Java Code with javac

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/maven/rps-maven
$ mvn compile
</code></pre>

#### Clean the build directory code with maven. 

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/maven/rps-maven
$ mvn clean
</code></pre>

#### Run the unit tests 

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/maven/rps-maven
$ mvn test
</code></pre>

<figure class="figure">
  <img src="/assets/merge-vs-build.jpg" alt="Build vs Merge with Maven Gradle and Git" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">Just because it will merge doesn't mean it will compile.</figcaption>
</figure>

#### Package the application as an executable JAR file

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/maven/rps-maven
$ mvn package
</code></pre>

If that gives you problems, just use the clean and install commands together.

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/maven/rps-maven
$ mvn clean install
</code></pre>

#### Run the Java JAR file

In the target folder you should see a JAR file. Run it! Just make sure you're in the target folder when you run this command.

Also, this runs on port 8080, so you may need to go to Windows Services and stop Jenkins. (3:45 in the YouTube video)


<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/maven/rps-maven/target
$ java -jar spock-lizard-1.0.jar
</code></pre>

When the app runs, it should be available at: http://localhost:8080 and http://localhost:8080/increasewins

CTRL+C in the BASH shell or command prompt kills the program.

#### Checkout and build the failure branch

When you try and build the failure branch you'll have tests that fail.

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/maven/rps-maven/
$ git add .
$ git commit -m "done"
$ git branch -a
$ git checkout failure
$ mvn clean install
</code></pre>

#### Checkout and build the broken branch

When you try to build the broken branch, you'll have a compiler error.

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/maven/rps-maven/
$ git add .
$ git commit -m "done"
$ git branch -a
$ git checkout broken
$ mvn clean install
</code></pre>

##### FindBugs, PMD and CheckStyle

If you really want to go crazy, run this command:

<pre><code> mvn compile checkstyle:checkstyle findbugs:findbugs pmd:pmd </code></pre>


Now check out the Maven cheat sheet to see all of the various Maven commands that are at your disposal.

<figure class="figure">
  <img src="https://pbs.twimg.com/media/C-KM9LfXkAAUFHP?format=jpg" alt="Maven Cheat Sheet" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">Maven Cheat Sheet.</figcaption>
</figure>

