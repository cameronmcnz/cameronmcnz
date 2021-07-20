---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Java Roshambo Assignment
blurb: Here's a fun little rock-paper-scissors game. Can you code it?
canonical: https://www.mcnz.com/2021/07/20/java-roshambo-assignment.html
---

<a class="btn btn-primary" href="https://www.mcnz.com/2021/07/20/back-to-basics-java.html">Assignment 1: The Basics</a>
<a class="btn btn-primary" href="https://www.mcnz.com/2021/07/20/java-number-guesser-assignment.html">Assignment 2: Guess a Number</a>
<a class="btn btn-primary" href="https://www.mcnz.com/2021/07/20/java-roshambo-assignment.html">Assignment 3: Roshambo!</a>

# Code it in Java

There's a rock-paper-scissors program embedded on <a href="http://www.mcnz.com">this page</a>t. Can you find it?

<a href="http://www.mcnz.com">https://www.mcnz.com/</a>

Could you code the equivalent in Java? 

In Java it won't look as pretty, but could you get the same basic functionality with the Scanner or JOptionPane?

Here are some tips:

- Create a Java class called Roshambo
- Add a main method
- Declare the required variables at the start of the main method
- For now, the server always chooses "Rock"
- Implement the logic to play the game once
- Then implement the logic to exit after 3 games
- Then add a static void method that prints out the results. You'll have to pass some data into it!

## Get Object Oriented!

Do you think a GameSummary class might be helpful? What properties would go in a GameSummary class?

#### I Like the JOptionPane

I'm not a big fan of the scanner. I like the JOptionPane better:

```
String prompt = "Will it be rock, paper or scissors?";
String input = JOptionPane.showInputDialog(prompt);
```

Try it out! The only problem is that it only returns a String, so you have to convert it to an int or double if that's what you need:

```
String prompt = "Will it be rock, paper or scissors?";
String input = JOptionPane.showInputDialog(prompt);
int number = Integer.parseInt(input);
```



### Review

What do you think? What was hard? Where did you get tripped up.
