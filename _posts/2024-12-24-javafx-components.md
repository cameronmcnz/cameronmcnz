---
layout: mcnz/basic-post
author: Cameron McKenzie
title: JavaFX Components and the VBox
blurb: Get familiar with the various JavaFX components!
---

# Part 3: JavaFX Layouts and Scenes

## Introduction to UI Components
JavaFX provides a wide variety of UI components that allow developers to create rich and interactive applications. Some of the most common components include:

- **Labels**: For displaying text.
- **Buttons**: For triggering actions.
- **TextFields**: For text input.
- **CheckBoxes**: For binary choices.
- **ComboBoxes**: For dropdown menus.
- **ListViews**: For displaying a list of items.
- **TableViews**: For displaying tabular data.
- **ProgressBars**: For showing progress.
- **MediaView**: For embedding media such as videos.

These components can be combined to create highly interactive user interfaces.

---

## Adding Multiple Components to a Scene
So far, we have only added a single component to a `Scene`. To add multiple components, we must first use a **layout component**. Layout components in JavaFX manage the positioning and arrangement of UI elements within the scene.

The simplest layout component is the **VBox**.

### What is a VBox?
A `VBox` is a layout component that arranges its child nodes (components) vertically, one below the other. It is useful when you want to create a simple, vertically-stacked layout for your UI.

### Key Features:
- Automatically adjusts the size of its children to fit within the layout.
- Provides spacing and padding options to control the appearance.
- Easy to use for forms, stacked buttons, or any vertically aligned content.

---

## Simple VBox Example
Let’s start with a basic example of a `VBox`. We will add the following components:
- A **Label**
- A **TextField**
- A **Button**

### Code Example:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class SimpleVBoxExample extends Application {
    @Override
    public void start(Stage stage) {
        // Create a VBox layout
        VBox vbox = new VBox();

        // Create a label
        Label label = new Label("Type Something");

        // Create a text field
        TextField textField = new TextField();

        // Create a button
        Button button = new Button("Click Me");

        // Add components to the VBox
        vbox.getChildren().addAll(label, textField, button);

        // Create a scene and set it on the stage
        Scene scene = new Scene(vbox, 300, 200);
        stage.setScene(scene);
        stage.setTitle("Simple VBox Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

This creates a simple, functional layout without any styling.

You can add multiple components to a `VBox` using either `addAll` or by adding them one at a time with `add`. Here's a quick comparison:

```java
// Adding multiple components at once using addAll
vbox.getChildren().addAll(label, textField, button);

// Adding components one at a time
vbox.getChildren().add(label);
vbox.getChildren().add(textField);
vbox.getChildren().add(button);
```

Both methods achieve the same result, but `addAll` is more concise when you have several components to add at once.

---

## Demonstrating the VBox Layout
Now let’s improve upon the basic layout by adding spacing, padding, and event handling. We’ll build a more interactive UI with the following components:
- A **Label** that initially says "Type Something".
- A **TextField** for user input.
- A **Button** that, when clicked, changes the text of the label to whatever is typed into the `TextField`.

### Code Example:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class VBoxExample extends Application {
    @Override
    public void start(Stage stage) {
        // Create a VBox layout
        VBox vbox = new VBox(10); // Vertical spacing of 10px
        // Add padding around the layout

        // Create a label
        Label label = new Label("Type Something");
        

        // Create a text field
        TextField textField = new TextField();
        textField.setPromptText("Enter text here...");

        // Create a button
        Button button = new Button("Click Me");
        button.setOnAction(e -> {
            String input = textField.getText();
            if (!input.isEmpty()) {
                label.setText(input);
            } else {
                label.setText("Type Something");
            }
        });

        // Add components to the VBox
        vbox.getChildren().addAll(label, textField, button);

        // Create a scene and set it on the stage
        Scene scene = new Scene(vbox, 300, 200);
        stage.setScene(scene);
        stage.setTitle("VBox Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

---

### Explanation:
1. **VBox Layout**:
   - The `VBox` arranges the `Label`, `TextField`, and `Button` vertically with 10px spacing between them.
   - Padding is added around the layout to create space between the components and the edges of the scene.

2. **Label and TextField**:
   - The `Label` displays a message that changes dynamically based on the user’s input.
   - The `TextField` allows users to type their input.

3. **Button Action**:
   - The `Button` uses an `EventHandler` to update the `Label` with the text entered in the `TextField` when clicked.

---

## Challenge: Add More Components
Experiment with adding more JavaFX components to the `VBox` layout. Try using the following components:
- **Spinner**
- **ProgressBar**
- **Slider**
- **CheckBox**
- **DatePicker**

This will help you explore how different components look and behave in a `VBox` layout.

### Possible Solution:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class Main extends Application {

    @Override
    public void start(Stage stage) {
        VBox vBoxLayout = new VBox(10);

        // Basic Controls
        vBoxLayout.getChildren().add(new Label("This is a Label"));
        vBoxLayout.getChildren().add(new Button("This is a Button"));
        vBoxLayout.getChildren().add(new TextField("This is a TextField"));
        vBoxLayout.getChildren().add(new PasswordField());
        vBoxLayout.getChildren().add(new TextArea("This is a TextArea"));
        vBoxLayout.getChildren().add(new CheckBox("This is a CheckBox"));
        vBoxLayout.getChildren().add(new Slider());
        vBoxLayout.getChildren().add(new ProgressBar(0.5));
        vBoxLayout.getChildren().add(new Hyperlink("This is a Hyperlink"));
        vBoxLayout.getChildren().add(new Spinner<>(0, 100, 50));

        // Date and Time Controls
        vBoxLayout.getChildren().add(new DatePicker());

        // Set the scene and display
        Scene scene = new Scene(vBoxLayout, 600, 800);
        stage.setScene(scene);
        stage.setTitle("JavaFX VBox Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

This solution demonstrates how to add multiple JavaFX components to a `VBox` layout. Try adding each component yourself and observe how they behave.
