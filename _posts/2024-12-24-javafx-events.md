---
layout: mcnz/basic-post
author: Cameron McKenzie
title: JavaFX Events, Controls and User Input
blurb: Here's how to respond to a simple button click in JavaFX
---

<div class="embed-responsive embed-responsive-16by9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/d4cDLBFbekw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

### **Part 2: Controls and User Input**

#### **Introduction to UI Controls**
JavaFX provides a variety of built-in controls to create interactive applications. Some of the most commonly used controls include:
- **Buttons**: Clickable elements to trigger actions.
- **TextFields**: Input fields for text.
- **Labels**: Non-editable text elements used for display.
- **CheckBoxes**: Selectable boxes for binary choices.
- **ComboBoxes**: Dropdown menus for selecting from a list of options.

---

#### **Event Handling**
JavaFX uses an event-driven model for interactivity. The `setOnAction` method is commonly used to handle user input or actions, such as button clicks. Event handlers define the logic that executes when the user interacts with a control.

##### **Example: Adding a Button to "Hello, World!"**
Let’s enhance the previous "Hello, World!" application by adding a button. When the button is clicked, the text toggles between "Click Me!" and "Let’s Learn JavaFX!"

##### **Code**:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.stage.Stage;

public class Main extends Application {
    @Override
    public void start(Stage stage) {
        Button button = new Button("Click Me!"); // Create a button
        button.setOnAction(e -> {               // Set button click action
            if (button.getText().equals("Click Me!")) {
                button.setText("Let’s Learn JavaFX!");
            } else {
                button.setText("Click Me!");
            }
        });

        Scene scene = new Scene(button, 400, 200); // Create a scene with the button
        stage.setScene(scene);                     // Set the scene on the stage
        stage.setTitle("Interactive Hello World"); // Set the title
        stage.show();                              // Show the stage
    }

    public static void main(String[] args) {
        launch(args); // Launch the JavaFX application
    }
}
```

##### **Explanation**:
1. **Button Creation**: A `Button` is added to the scene.
2. **Event Handling**: The `setOnAction` method toggles the button text on click.

---

#### **Exercise: Build a Simple Form**
Create a JavaFX application with:
- A **TextField** for user input.
- A **Button** to submit the form.
- A **Label** to display the confirmation message.

This exercise reinforces using controls, event handling, and layouts in JavaFX.

--- 

Let me know if you'd like any further details or edits!

Congratulations! You’ve set up JavaFX and created your first application. In the next part, you’ll dive into layouts and scenes to design more complex user interfaces.


