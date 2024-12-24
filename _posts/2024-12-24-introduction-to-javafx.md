---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Introduction to JavaFX
blurb: Here's an introduction on how to learn JavaFX.
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/d4cDLBFbekw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

# Part 1: Introduction to JavaFX

## What is JavaFX?
JavaFX is a modern framework for building rich client applications in Java. It was introduced by Sun Microsystems in 2007 as a successor to Swing and AWT, and it became part of the official JDK with Java SE 7. Designed to offer a more advanced and flexible way to build user interfaces, JavaFX supports 2D and 3D graphics, animation, and media playback.

### Key Features:
- **Rich UI Components**: Includes a wide variety of prebuilt controls like buttons, text fields, and tables.
- **Hardware Acceleration**: Utilizes GPU for better performance with graphics and animations.
- **CSS Styling**: Allows styling of the UI using CSS, similar to web development.
- **FXML Support**: Provides a declarative way to design interfaces with XML.

### Comparison with Swing and AWT:
| Feature         | AWT               | Swing               | JavaFX                 |
|-----------------|-------------------|---------------------|------------------------|
| UI Components   | Basic and limited | Enhanced and customizable | Modern and feature-rich |
| Graphics        | Limited           | Better than AWT     | Advanced with GPU support |
| Styling         | None              | Basic               | Full CSS support        |
| Declarative UI  | No                | No                  | Yes (FXML)             |

JavaFX is ideal for applications requiring a modern UI, animations, and multimedia capabilities.

---

## Setting up JavaFX

### Installing JDK with JavaFX Support:
1. **Download JDK**:
   - Ensure you download a JDK version that includes JavaFX support or download JavaFX SDK separately from [openjfx.io](https://openjfx.io).
2. **Environment Configuration**:
   - If using a standalone JavaFX SDK, set the `PATH` and `JAVA_HOME` to include the JavaFX libraries.

### Configuring IDEs:

#### IntelliJ IDEA:
1. **Create a New Project**:
   - Go to `File > New Project` and select `JavaFX` as the template.
2. **Add JavaFX SDK**:
   - Go to `File > Project Structure > Libraries` and add the JavaFX SDK path.
3. **VM Options**:
   - In `Run > Edit Configurations`, set the VM options for JavaFX:
     ```
     --module-path "path_to_javafx_lib" --add-modules javafx.controls,javafx.fxml
     ```

#### Eclipse:
1. **Install e(fx)clipse Plugin**:
   - Go to `Help > Eclipse Marketplace` and search for "e(fx)clipse".
   - Install and restart Eclipse.
2. **Create a JavaFX Project**:
   - Go to `File > New > Other > JavaFX Project`.
3. **Configure JavaFX SDK**:
   - Go to `Project > Properties > Java Build Path` and add the JavaFX SDK libraries.

---

## Creating Your First JavaFX App

Here is a simple "Hello, World!" application in JavaFX.

### Steps:
1. **Create a Java Class**:
   - Create a class that extends `Application`.

2. **Override the `start` Method**:
   - The `start` method is the entry point for JavaFX applications. It takes a `Stage` (the main window) as a parameter.

3. **Create and Set a Scene**:
   - Use a `Scene` to define your UI layout.

### Example Code:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;

public class HelloWorldApp extends Application {
    @Override
    public void start(Stage stage) {
        // Create a label to display "Hello, World!"
        Label label = new Label("Hello, World!");

        // Create a scene with the label
        Scene scene = new Scene(label, 400, 200);

        // Set the scene on the stage and display it
        stage.setScene(scene);
        stage.setTitle("Hello, World!");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

### Running the Application:
1. **Compile and Run**:
   - Use your IDE’s `Run` button or compile and run via the terminal.
2. **View the Result**:
   - A window should open with "Hello, World!" displayed.

---

Congratulations! You’ve set up JavaFX and created your first application. In the next part, you’ll dive into layouts and scenes to design more complex user interfaces.


#### Gitflow Release Finished

You want those fixes that would happen here to make sure they find their way into development too but of course it gets put into master and now one last thing git tag dash l for list and you see boom we've got another tag in there 0 2 0 because it was 0 2 0 that we released into the master and the develop branches.

And there you go, that's how the get flow release branch works. That's how easy it is to work with the gitflow release branch in git flow. 

If you enjoyed that tutorial why don't you head over to the [serverside.com](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/init-Gitflow-example-workflow-tutorial). I'm the editor in chief over there we've got lots of great tutorials on git github git flow devops enterprise software development you name it if you're interested in my personal antics you can always follow me on twitter at cameronmcnz and subscribe on the youtube
