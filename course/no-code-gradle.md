---
layout: mcnz/hidden-post
author: Cameron McKenzie
title: Lab 4 - No Code Gradle
blurb: Here's the Gradle lab with code from GitHub
canonical: https://www.mcnz.com/course/no-code-gradle.html
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
<iframe width="560" height="315" src="https://www.youtube.com/embed/rY-MrvpZ6xU" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

# Introduction to Gradle

Here's Lab 4 with a twist. Instead of writing your own code, why not pull it from GitHub, and then build it with Gradle, just like you would do if you were a DevOps engineer out in the field.

## Part 1-3

Create a folder under C:\workspace\labs\gradle and in that directory clone a GitHub repo:

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/
$ git clone https://github.com/cameronmcnz/MyProject.git
</code></pre>
You may need to then move into the MyProject directory

<pre><code>cd My*</code></pre>

### Compile Java Code with javac

From the MyProject directory, look at the BadJava.java file. Then compile it with the Java compiler:

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject
$ javac BadJava.java
</code></pre>

Then run the bytecode

<pre><code>$ java BadJava</code></pre>

### Gradle Tasks

See what Gradle tasks are available:

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject
$ gradle tasks
</code></pre>

Then tell Gradle that you're all about Java:

<pre><code>apply plugin: 'java'</code></pre>

Now run the tasks again and note the difference.

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject
$ gradle tasks
</code></pre>

<figure class="figure">
  <img src="/assets/merge-vs-build.jpg" alt="Build vs Merge with Maven Gradle and Git" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">Just because it will merge doesn't mean it will compile.</figcaption>
</figure>

### Compile with Gradle

Compile your code with Gradle:

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject (part7)
$ gradle classes
</code></pre>
Now clean up your workspace:

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject (part7)
$ gradle clean
</code></pre>

Now build a JAR file:

<pre><code>wasadmin@CLASSPC MINGW64 /c/Workspace/labs/gradle/MyProject (part7)
$ gradle build
</code></pre>

And clean up again:

<pre><code>$ gradle clean
</code></pre>

### Switch Branches

Add and commit your changes:

<pre><code>git add .
git commit -m "done for now"
</code></pre>

Then switch branches:

<pre><code>git checkout part5
</code></pre>

### Part 5

Update your gradle file according to the lab guide.

Commands to issue include:

<pre><code>gradle build
gradle -q run
</code></pre>

### Switch branches

To switch branches, add and commit again. Then do the checkout:

<pre><code>git add .
git commit -m "done again"

git checkout part7
</code></pre>

### Run Tests

Look at the code added under the test folders. Follow section 7 in the book and then run the test command. Note that it will fail.

<pre><code>gradle test</code></pre>

Fix the test files so the test will pass. Then run your tests again.

<pre><code>gradle test</code></pre>

That just about covers it!

<figure class="figure">
  <img src="https://miro.medium.com/max/700/1*E5JMRbW525OHTa1Op7dGGA.png" alt="Java Features" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">Gradle Lifecycle.</figcaption>
</figure>

<figure class="figure">
  <img src="https://pbs.twimg.com/media/C-KM9LfXkAAUFHP?format=jpg" alt="Java Features" class="img-fluid mx-auto d-block img-thumbnail rounded ">
  <figcaption class="figure-caption">Maven Cheat Sheet.</figcaption>
</figure>

