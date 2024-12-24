---
layout: mcnz/basic-post
author: Cameron McKenzie
title: JavaFX Layouts
blurb: Here are the various layouts you'll want to use with JavaFX.
---

# Part 5: Layouts

## Why Use Layouts in JavaFX?

Layouts in JavaFX are essential for arranging UI components within a scene. They define the structure and placement of nodes and help create flexible, responsive, and visually appealing user interfaces.

### Common Types of Layouts

1. **VBox (Vertical Box)**:
   - Aligns child nodes vertically.
   - Ideal for forms and stacked elements.

2. **HBox (Horizontal Box)**:
   - Aligns child nodes horizontally.
   - Useful for toolbars or horizontal button groups.

3. **GridPane**:
   - Organizes nodes in a grid structure with rows and columns.
   - Suitable for creating structured layouts like forms or calendars.

4. **BorderPane**:
   - Divides the scene into five regions: top, bottom, left, right, and center.
   - Perfect for layouts that have a header, footer, and central content.

5. **StackPane**:
   - Layers nodes on top of each other.
   - Useful for overlays and layered content.

---

## Example: HBox Layout

Let’s create an `HBox` layout with three labels. Each label will have a unique style.

### Code Example:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;

public class HBoxExample extends Application {
    @Override
    public void start(Stage stage) {
        HBox hbox = new HBox(10); // Horizontal spacing of 10px
        hbox.setStyle("-fx-padding: 10 10 10 10;");

        Label label1 = new Label("Left Aligned");
        label1.setStyle("-fx-background-color: lightblue; -fx-alignment: center; -fx-padding: 20; -fx-font-size: 14px;");
        label1.setMaxWidth(Double.MAX_VALUE);

        Label label2 = new Label("Center Aligned");
        label2.setStyle("-fx-background-color: lightgreen; -fx-alignment: center; -fx-padding: 20; -fx-font-size: 14px;");
        label2.setMaxWidth(Double.MAX_VALUE);

        Label label3 = new Label("Right Aligned");
        label3.setStyle("-fx-background-color: lightpink; -fx-alignment: center; -fx-padding: 20; -fx-font-size: 14px;");
        label3.setMaxWidth(Double.MAX_VALUE);

        hbox.getChildren().addAll(label1, label2, label3);

        Scene scene = new Scene(hbox, 600, 200);
        stage.setScene(scene);
        stage.setTitle("HBox Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

---

## Example: GridPane Layout

Let’s create a 3x4 `GridPane`. Each cell will display its coordinates.

### Code Example:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

public class GridPaneExample extends Application {
    @Override
    public void start(Stage stage) {
        GridPane grid = new GridPane();
        grid.setHgap(10); // Horizontal gap
        grid.setVgap(10); // Vertical gap
        grid.setStyle("-fx-padding: 10;");

        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 4; col++) {
                Label label = new Label("Row " + row + ", Col " + col);
                label.setStyle("-fx-background-color: lightyellow; -fx-padding: 10; -fx-font-size: 12px;");
                grid.add(label, col, row);
            }
        }

        Scene scene = new Scene(grid, 600, 400);
        stage.setScene(scene);
        stage.setTitle("GridPane Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

---

## Example: BorderPane Layout

Let’s create a `BorderPane` with different colors in each section. The top and bottom labels will expand to fill horizontally, the left and right labels will fill vertically, and the center label will fill the remaining space.

### Code Example:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;

public class Main extends Application {
    @Override
    public void start(Stage stage) {
        BorderPane borderPane = new BorderPane();

        Label top = new Label("Top");
        top.setStyle("-fx-background-color: lightblue; -fx-padding: 20; -fx-alignment: center;");
        top.setMaxWidth(Double.MAX_VALUE);
        top.setMinHeight(100);

        Label bottom = new Label("Bottom");
        bottom.setStyle("-fx-background-color: lightgreen; -fx-padding: 20; -fx-alignment: center;");
        bottom.setMaxWidth(Double.MAX_VALUE);
        bottom.setMinHeight(100);

        Label left = new Label("Left");
        left.setStyle("-fx-background-color: lightpink; -fx-padding: 20; -fx-alignment: center;");
        left.setMaxHeight(Double.MAX_VALUE);
        left.setMinWidth(150);

        Label right = new Label("Right");
        right.setStyle("-fx-background-color: lightyellow; -fx-padding: 20; -fx-alignment: center;");
        right.setMaxHeight(Double.MAX_VALUE);
        right.setMinWidth(150);

        Label center = new Label("Center");
        center.setStyle("-fx-background-color: lightcoral; -fx-padding: 20; -fx-alignment: center;");

        borderPane.setTop(top);
        borderPane.setBottom(bottom);
        borderPane.setLeft(left);
        borderPane.setRight(right);
        borderPane.setCenter(center);

        Scene scene = new Scene(borderPane, 600, 400);
        stage.setScene(scene);
        stage.setTitle("BorderPane Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

---

## Advanced: StackPane Layout

The `StackPane` layers nodes on top of each other. Below is a simple example.

### Code Example:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class StackPaneExample extends Application {
    @Override
    public void start(Stage stage) {
        StackPane stackPane = new StackPane();

        Label backgroundLabel = new Label("Background");
        backgroundLabel.setStyle("-fx-background-color: lightgray; -fx-padding: 50; -fx-alignment: center;");

        Label middleLabel = new Label("Middle Layer");
        middleLabel.setStyle("-fx-background-color: lightblue; -fx-padding: 30; -fx-alignment: center;");

        Label foregroundLabel = new Label("Foreground");
        foregroundLabel.setStyle("-fx-background-color: lightgreen; -fx-padding: 10; -fx-alignment: center;");

        stackPane.getChildren().addAll(backgroundLabel, middleLabel, foregroundLabel);

        Scene scene = new Scene(stackPane, 400, 400);
        stage.setScene(scene);
        stage.setTitle("StackPane Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

---

## Challenge: HBox with Number Guesser

Create an `HBox` with three labels:
1. The left and right labels should have a black background.
2. The middle label should include the "Number Guesser" example.

### Solution:
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;

public class NumberGuesserHBox extends Application {
    @Override
    public void start(Stage stage) {
        HBox hbox = new HBox(10);
        hbox.setStyle("-fx-padding: 10;");

        Label left = new Label();
        left.setStyle("-fx-background-color: black; -fx-min-width: 100px; -fx-min-height: 100px;");

        Label right = new Label();
        right.setStyle("-fx-background-color: black; -fx-min-width: 100px; -fx-min-height: 100px;");

        // Middle Label with Number Guesser
        Label prompt = new Label("Guess a number:");
        TextField input = new TextField();
        Button button = new Button("Submit");
        Label result = new Label();
        button.setOnAction(e -> {
            try {
                int guess = Integer.parseInt(input.getText());
                result.setText(guess == 5 ? "Correct!" : "Try Again");
            } catch (NumberFormatException ex) {
                result.setText("Invalid Input");
            }
        });

        HBox middle = new HBox(10, prompt, input, button, result);
        middle.setStyle("-fx-padding: 10;");

        hbox.getChildren().addAll(left, middle, right);

        Scene scene = new Scene(hbox, 600, 200);
        stage.setScene(scene);
        stage.setTitle("HBox Number Guesser");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

