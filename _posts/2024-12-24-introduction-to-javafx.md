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

The provided JavaFX code demonstrates a simple "Hello, World!" application. Here's what each part of the code does:

### Code Breakdown:

1. **Import Statements**:
   - `javafx.application.Application`: The base class for JavaFX applications.
   - `javafx.scene.Scene`: Represents the container for all content in a JavaFX application.
   - `javafx.scene.control.Label`: A UI control to display text.
   - `javafx.stage.Stage`: Represents the main window (or primary stage) of the application.

2. **Main Class**:
   ```java
   public class HelloWorldApp extends Application {
   ```
   - The class extends `Application`, making it a JavaFX application. This is required to use the JavaFX framework.

3. **`start` Method**:
   ```java
   public void start(Stage stage) {
   ```
   - The `start` method is the entry point of the JavaFX application. It is automatically called after the application is launched.

4. **Creating a Label**:
   ```java
   Label label = new Label("Hello, World!");
   ```
   - A `Label` is created to display the text "Hello, World!" on the screen.

5. **Creating a Scene**:
   ```java
   Scene scene = new Scene(label, 400, 200);
   ```
   - A `Scene` is created to hold the `Label`. The scene defines the width (400) and height (200) of the application window.

6. **Setting the Scene on the Stage**:
   ```java
   stage.setScene(scene);
   ```
   - The `Scene` is set on the `Stage`, which is the main window of the application.

7. **Setting the Window Title**:
   ```java
   stage.setTitle("Hello, World!");
   ```
   - The title of the `Stage` is set to "Hello, World!" which appears in the title bar of the application window.

8. **Displaying the Stage**:
   ```java
   stage.show();
   ```
   - The `show` method makes the `Stage` visible on the screen.

9. **`main` Method**:
   ```java
   public static void main(String[] args) {
       launch(args);
   }
   ```
   - The `main` method is the entry point of the Java application. It calls `launch(args)` to start the JavaFX application, which initializes the JavaFX runtime and calls the `start` method.

### Execution Flow:
1. The `main` method launches the application.
2. The JavaFX runtime initializes and calls the `start` method.
3. A `Label` is created and added to a `Scene`.
4. The `Scene` is set on the `Stage`, which is then shown on the screen.
5. The application displays a window with "Hello, World!" in the center.

### Result:
When you run the program, a window opens with the title "Hello, World!" and the text "Hello, World!" displayed within it. The window size is 400 pixels wide and 200 pixels high.

Congratulations! You’ve set up JavaFX and created your first application. In the next part, you’ll dive into layouts and scenes to design more complex user interfaces.


