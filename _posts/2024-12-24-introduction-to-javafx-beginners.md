---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Introduction to JavaFX Events
blurb: Here's how to respond to a simple button click in JavaFX
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/d4cDLBFbekw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

Here is Part 1 and Part 2 of the course:

---

### **Part 1: Introduction to JavaFX**

#### **What is JavaFX?**
JavaFX is a modern framework for building rich client applications in Java. It was introduced by Sun Microsystems in 2007 as a successor to Swing and AWT, and it became part of the official JDK with Java SE 7. Designed to offer a more advanced and flexible way to build user interfaces, JavaFX supports 2D and 3D graphics, animation, and media playback.

##### **Key Features**:
- **Rich UI Components**: Includes a wide variety of prebuilt controls like buttons, text fields, and tables.
- **Hardware Acceleration**: Utilizes GPU for better performance with graphics and animations.
- **CSS Styling**: Allows styling of the UI using CSS, similar to web development.
- **FXML Support**: Provides a declarative way to design interfaces with XML.

##### **Comparison with Swing and AWT**:
| Feature         | AWT               | Swing               | JavaFX                 |
|-----------------|-------------------|---------------------|------------------------|
| UI Components   | Basic and limited | Enhanced and customizable | Modern and feature-rich |
| Graphics        | Limited           | Better than AWT     | Advanced with GPU support |
| Styling         | None              | Basic               | Full CSS support        |
| Declarative UI  | No                | No                  | Yes (FXML)             |

JavaFX is ideal for applications requiring a modern UI, animations, and multimedia capabilities.

---

#### **Setting up JavaFX**

##### **Installing JDK with JavaFX Support**:
1. **Download JDK**:
   - Ensure you download a JDK version that includes JavaFX support or download JavaFX SDK separately from [openjfx.io](https://openjfx.io).
2. **Environment Configuration**:
   - If using a standalone JavaFX SDK, set the `PATH` and `JAVA_HOME` to include the JavaFX libraries.

##### **Configuring IDEs**:

**IntelliJ IDEA**:
1. **Create a New Project**:
   - Go to `File > New Project` and select `JavaFX` as the template.
2. **Add JavaFX SDK**:
   - Go to `File > Project Structure > Libraries` and add the JavaFX SDK path.
3. **VM Options**:
   - In `Run > Edit Configurations`, set the VM options for JavaFX:
     ```text
     --module-path "path_to_javafx_lib" --add-modules javafx.controls,javafx.fxml
     ```

**Eclipse**:
1. **Install e(fx)clipse Plugin**:
   - Go to `Help > Eclipse Marketplace` and search for "e(fx)clipse".
   - Install and restart Eclipse.
2. **Create a JavaFX Project**:
   - Go to `File > New > Other > JavaFX Project`.
3. **Configure JavaFX SDK**:
   - Go to `Project > Properties > Java Build Path` and add the JavaFX SDK libraries.

---

#### **Creating Your First JavaFX App**

Below is a simple "Hello, World!" application in JavaFX.

##### **Code**:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;

public class HelloWorldApp extends Application {
    @Override
    public void start(Stage stage) {
        Label label = new Label("Hello, World!"); // Create a label
        Scene scene = new Scene(label, 400, 200); // Create a scene with the label
        stage.setScene(scene);                    // Set the scene on the stage
        stage.setTitle("Hello, World!");          // Set the title
        stage.show();                             // Show the stage
    }

    public static void main(String[] args) {
        launch(args); // Launch the JavaFX application
    }
}
```

##### **Explanation**:
1. **Main Class**: Extends `Application`, making it a JavaFX application.
2. **Label**: Displays "Hello, World!" text.
3. **Scene**: Holds the `Label` and defines the size of the application window.
4. **Stage**: Represents the main window of the application.

---
