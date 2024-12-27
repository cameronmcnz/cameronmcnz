---
layout: mcnz/basic-post
author: Cameron McKenzie
title: JavaFX Number Guessing Game
blurb: Learn how to code JavaFX apps with this Number Guessing game!
---


```
package com.mcnz.javafx;

import java.util.Random;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class NumberGuesser extends Application 
{ 
    int magicNumber;
    int numberOfTries;

  @Override
  public void start(Stage stage) {
      
      var promptLabel = new Label("Guess a number between 1 and 10!");
      var inputField = new TextField();
      var guessButton = new Button("Guess");
      var feedbackLabel = new Label();

      var layout = new VBox(10, promptLabel, inputField, guessButton, feedbackLabel);

      var scene = new Scene(layout, 300, 200);
      stage.setTitle("Number Guessing Game");
      stage.setScene(scene);
      stage.show();

      Random random = new Random();
      magicNumber = random.nextInt(10) + 1;

      guessButton.setOnAction(e -> {
            String input = inputField.getText();
            int guess = Integer.parseInt(input);
            numberOfTries++;
            if (guess < magicNumber) {
                feedbackLabel.setText("Guess Higher!");
                guessButton.setText("Guess again");
            }
            if (guess > magicNumber) {
                feedbackLabel.setText("Guess Lower!");
                guessButton.setText("Guess again");
            }
            if (guess == magicNumber){
                feedbackLabel.setText("You guessed it right in " + numberOfTries + " tries!");
                guessButton.setText("Play again?");
                magicNumber = random.nextInt(10) + 1;
            }
            inputField.clear();
        });
  }

  public static void main(String[] args) {
      Application.launch(NumberGuesser.class, args);
  }
} 
```
