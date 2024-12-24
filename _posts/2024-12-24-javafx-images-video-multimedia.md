---
layout: mcnz/basic-post
author: Cameron McKenzie
title: JavaFX, Images, Video and Multimedia
blurb: Here's how to include images and multimedia in your JavaFX apps.
---

# Part 6: Working with Multimedia

## Introduction to Multimedia in JavaFX

JavaFX makes it easy to work with images and multimedia, enabling you to create rich and interactive user interfaces.

### Working with Images

#### Important Methods in `Image` and `ImageView`

**`Image` Class:**
1. **`Image(String url)`**: Creates an image from the specified file path or URL.
2. **`getWidth()`**: Returns the width of the image.
3. **`getHeight()`**: Returns the height of the image.

**`ImageView` Class:**
1. **`setImage(Image image)`**: Sets the image to display in the `ImageView`.
2. **`setFitWidth(double value)`**: Resizes the image's width while maintaining the aspect ratio.
3. **`setFitHeight(double value)`**: Resizes the image's height while maintaining the aspect ratio.
4. **`setPreserveRatio(boolean value)`**: Ensures the image's aspect ratio is preserved during resizing.
5. **`setSmooth(boolean value)`**: Applies a smoothing effect when resizing.

---

## Very Simple Image Example

Let’s start with a very simple application that displays one image directly on the scene without using layouts.

### Code Example:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.stage.Stage;

public class SimpleImageExample extends Application {
    @Override
    public void start(Stage stage) {
        // Load the image
        Image rockImage = new Image("file:rock.png");

        // Create an ImageView to display the image
        ImageView imageView = new ImageView(rockImage);
        imageView.setFitWidth(200);
        imageView.setFitHeight(200);

        // Add the ImageView directly to the scene
        Scene scene = new Scene(imageView, 400, 400);
        stage.setScene(scene);
        stage.setTitle("Simple Image Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

---

## Example: Displaying Images

Let’s now display images of rock, paper, and scissors next to each other and add actions for when the user clicks on them.

### Code Example:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class ImageExample extends Application {
    @Override
    public void start(Stage stage) {
        // Load images
        Image rockImage = new Image("file:rock.png");
        Image paperImage = new Image("file:paper.png");
        Image scissorsImage = new Image("file:scissors.png");

        // Create ImageViews
        ImageView rockView = new ImageView(rockImage);
        ImageView paperView = new ImageView(paperImage);
        ImageView scissorsView = new ImageView(scissorsImage);

        // Set image sizes
        rockView.setFitWidth(100);
        rockView.setFitHeight(100);
        paperView.setFitWidth(100);
        paperView.setFitHeight(100);
        scissorsView.setFitWidth(100);
        scissorsView.setFitHeight(100);

        // Create labels to show clicked item
        Label resultLabel = new Label("Click an image");

        // Add click actions
        rockView.setOnMouseClicked(e -> resultLabel.setText("You clicked Rock"));
        paperView.setOnMouseClicked(e -> resultLabel.setText("You clicked Paper"));
        scissorsView.setOnMouseClicked(e -> resultLabel.setText("You clicked Scissors"));

        // Create layout
        HBox hbox = new HBox(20, rockView, paperView, scissorsView);
        VBox layout = new VBox(10, hbox, resultLabel);

        Scene scene = new Scene(layout, 400, 300);
        stage.setScene(scene);
        stage.setTitle("Rock Paper Scissors");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

---

### Working with Media

#### Important Methods in `Media`, `MediaPlayer`, and `MediaView`

**`Media` Class:**
1. **`Media(String source)`**: Loads a media file from a specified path or URL.

**`MediaPlayer` Class:**
1. **`play()`**: Starts or resumes playback.
2. **`pause()`**: Pauses playback.
3. **`stop()`**: Stops playback and resets to the beginning.
4. **`setVolume(double value)`**: Sets the playback volume (range: 0.0 to 1.0).
5. **`setAutoPlay(boolean value)`**: Automatically starts playback when the media is loaded.

**`MediaView` Class:**
1. **`setMediaPlayer(MediaPlayer player)`**: Associates a `MediaPlayer` with the `MediaView`.
2. **`setFitWidth(double value)`**: Sets the width of the video display area.
3. **`setFitHeight(double value)`**: Sets the height of the video display area.

---

## Example: Playing Media

Let’s create an app that plays an MP4 video.

### Code Example:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.stage.Stage;

public class MediaExample extends Application {
    @Override
    public void start(Stage stage) {
        // Load media
        Media media = new Media("file:congratulations.mp4");
        MediaPlayer mediaPlayer = new MediaPlayer(media);

        // Create a MediaView and associate it with the MediaPlayer
        MediaView mediaView = new MediaView(mediaPlayer);

        // Auto play the video
        mediaPlayer.setAutoPlay(true);

        // Add MediaView directly to the scene
        Scene scene = new Scene(mediaView, 800, 600);
        stage.setScene(scene);
        stage.setTitle("Media Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

---

## Working with JavaFX Alerts

The `Alert` class in JavaFX provides a convenient way to display pop-up messages to the user. Alerts are often used to communicate important information, errors, or results to the user in a graphical manner.

### Types of Alerts
1. **INFORMATION**: Used to display general information to the user.
2. **WARNING**: Alerts the user about potential issues.
3. **ERROR**: Displays error messages.
4. **CONFIRMATION**: Used for user confirmation dialogs.
5. **NONE**: A plain dialog without predefined icons or styles.

### How to Create and Use an Alert
- Create an instance of `Alert` and specify the type.
- Set the title, header text, and content text.
- Use `show()` to display the alert or `showAndWait()` to pause the application until the alert is closed.

### Example Code:
```java
Alert alert = new Alert(Alert.AlertType.INFORMATION);
alert.setTitle("Sample Alert");
alert.setHeaderText("This is the header text");
alert.setContentText("This is the content of the alert.");
alert.showAndWait();
```

---

## Example: Rock Paper Scissors Game

Let’s create an app that displays rock, paper, scissors images, allows the player to choose, and shows the result in a pop-up. The server will always choose rock.

---

## Challenge: Add Video to the Pop-Up

Modify the Rock Paper Scissors game so that if the player wins, the pop-up also plays a congratulatory video.

### Solution:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.HBox;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.stage.Stage;

public class RockPaperScissorsWithVideo extends Application {
    @Override
    public void start(Stage stage) {
        // Load images
        Image rockImage = new Image("file:rock.png");
        Image paperImage = new Image("file:paper.png");
        Image scissorsImage = new Image("file:scissors.png");

        // Create ImageViews
        ImageView rockView = new ImageView(rockImage);
        ImageView paperView = new ImageView(paperImage);
        ImageView scissorsView = new ImageView(scissorsImage);

        // Set image sizes
        rockView.setFitWidth(100);
        rockView.setFitHeight(100);
        paperView.setFitWidth(100);
        paperView.setFitHeight(100);
        scissorsView.setFitWidth(100);
        scissorsView.setFitHeight(100);

        // Add click actions
        rockView.setOnMouseClicked(e -> showResult("Rock"));
        paperView.setOnMouseClicked(e -> showResult("Paper"));
        scissorsView.setOnMouseClicked(e -> showResult("Scissors"));

        // Create layout
        HBox hbox = new HBox(20, rockView, paperView, scissorsView);

        Scene scene = new Scene(hbox, 400, 200);
        stage.setScene(scene);
        stage.setTitle("Rock Paper Scissors with Video");
        stage.show();
    }

    private void showResult(String playerChoice) {
        String serverChoice = "Rock";
        String result;
        boolean isWin = false;
        if (playerChoice.equals(serverChoice)) {
            result = "It's a Tie!";
        } else if (playerChoice.equals("Paper")) {
            result = "You Win!";
            isWin = true;
        } else {
            result = "You Lose!";
        }

        Alert alert = new Alert(AlertType.INFORMATION);
        alert.setTitle("Game Result");
        alert.setHeaderText(null);
        alert.setContentText(result);
        alert.showAndWait();

        if (isWin) {
            playVideo();
        }
    }

    private void playVideo() {
        Stage videoStage = new Stage();
        Media media = new Media("file:congratulations.mp4");
        MediaPlayer mediaPlayer = new MediaPlayer(media);
        MediaView mediaView = new MediaView(mediaPlayer);

        mediaPlayer.setAutoPlay(true);
        Scene scene = new Scene(mediaView, 800, 600);
        videoStage.setScene(scene);
        videoStage.setTitle("Congratulations Video");
        videoStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```
