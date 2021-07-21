---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Java NumberGuesser Assignment
blurb: How well do you know your Java basics? Try your hand at coding the numberguesser!
canonical: https://www.mcnz.com/2021/07/20/java-number-guesser-assignment.html
---
<a class="btn btn-primary" href="https://www.mcnz.com/2021/07/20/back-to-basics-java.html">Assignment 1: The Basics</a>
<a class="btn btn-primary" href="https://www.mcnz.com/2021/07/20/java-number-guesser-assignment.html">Assignment 2: Guess a Number</a>
<a class="btn btn-primary" href="https://www.mcnz.com/2021/07/20/java-roshambo-assignment.html">Assignment 3: Roshambo!</a>

# Code it in Java

Take a look at this little web application:

https://www.mcnz.com/course/numberguesser.html

Could you code the equivalent in Java? 

In Java it won't look as pretty, but could you get the same basic functionality with the Scanner or JInputPane?

Here are some tips:

- Create a Java class called NumberGuesser
- Add a main method
- Hard code the magic number to 5 for now
- Keep track of the number of guesses
- At the start of the main method, declare the variables you'll need, like the magicNumber and the numberOfAttempts

## Refactor it!

Create a new, static, void method that prints out the results when the game is completed.

You will need to pass in two arguments at least: The magicNumber and the numberOfAttempts

### Randoms

There's a class called java.util.Random that generates random numbers. Any idea how to integrate it in?

Here's a hint:
```
Random random = new Random();
int rand = random.nextInt();
```

#### Play the name game!

Get the users name before you play the game. Then, when you print out the results, make the message personalized!

#### Is there a GameData object here?

Say someone wanted you to get 'object oriented.' Is there any data in the application that could be logically grouped together in a single object?

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














