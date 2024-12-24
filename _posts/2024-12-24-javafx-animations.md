---
layout: mcnz/basic-post
author: Cameron McKenzie
title: JavaFX Animations
blurb: Want to learn some cool JavaFX tricks? Here are 10 animations you can start using right away!
---

# Part 7: Animations and Effects

## Introduction to JavaFX Animations and Effects

Animations are a vital aspect of modern user interfaces, providing a dynamic and engaging experience. JavaFX offers powerful tools for creating animations and applying effects to your applications.

### Key Components of Animations in JavaFX

1. **Timeline**:
   - A flexible way to create animations by defining keyframes.
   - Works well for property changes over time.

2. **Transitions**:
   - Predefined animation types for common use cases:
     - **FadeTransition**: Animates the opacity of a node.
     - **RotateTransition**: Rotates a node around its pivot point.
     - **ScaleTransition**: Changes the scale (size) of a node.
     - **TranslateTransition**: Moves a node to a different position.
     - **SequentialTransition** and **ParallelTransition**: Combine multiple animations.

3. **Visual Effects**:
   - JavaFX provides effects like **Blur**, **Shadow**, and **Reflection** to enhance the visual appeal of nodes.

4. **Duration**:
   - Defines the length of time an animation takes.

5. **Interpolator**:
   - Controls the pacing of animations (e.g., linear, ease-in, ease-out).

---

### Example 1: Fade In and Out
```java
import javafx.animation.*;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;
import javafx.util.Duration;

public class FadeAnimation extends Application {
    @Override
    public void start(Stage stage) {
        Label label = new Label("Fade In and Out");
        label.setStyle("-fx-font-size: 24px;");

        FadeTransition fade = new FadeTransition(Duration.seconds(2), label);
        fade.setFromValue(0);
        fade.setToValue(1);
        fade.setCycleCount(Animation.INDEFINITE);
        fade.setAutoReverse(true);

        Scene scene = new Scene(label, 400, 200);
        stage.setScene(scene);
        stage.setTitle("Fade Animation");
        stage.show();

        fade.play();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**Synopsis**:
This example uses a `FadeTransition` to make a label fade in and out repeatedly. The `setFromValue` and `setToValue` properties control the opacity range, while `setCycleCount(Animation.INDEFINITE)` makes the animation loop forever. This is a great way to draw attention to a specific UI element.

---

### Example 2: Rotating Square
```java
import javafx.animation.*;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.stage.Stage;
import javafx.util.Duration;

public class RotateAnimation extends Application {
    @Override
    public void start(Stage stage) {
        Rectangle rectangle = new Rectangle(100, 100, Color.BLUE);

        RotateTransition rotate = new RotateTransition(Duration.seconds(2), rectangle);
        rotate.setByAngle(360);
        rotate.setCycleCount(Animation.INDEFINITE);

        Scene scene = new Scene(rectangle, 400, 400);
        stage.setScene(scene);
        stage.setTitle("Rotate Animation");
        stage.show();

        rotate.play();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**Synopsis**:
This example uses a `RotateTransition` to rotate a square endlessly around its center. The `setByAngle(360)` specifies a full rotation, and the `setCycleCount(Animation.INDEFINITE)` ensures it keeps spinning. It’s a fun, eye-catching effect for loaders or visual indicators.

---

### Example 3: Bouncing Ball
```java
import javafx.animation.*;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.stage.Stage;
import javafx.util.Duration;

public class BouncingBall extends Application {
    @Override
    public void start(Stage stage) {
        Circle ball = new Circle(20, Color.RED);

        TranslateTransition bounce = new TranslateTransition(Duration.seconds(1), ball);
        bounce.setByY(200);
        bounce.setCycleCount(Animation.INDEFINITE);
        bounce.setAutoReverse(true);

        Scene scene = new Scene(ball, 400, 400);
        stage.setScene(scene);
        stage.setTitle("Bouncing Ball");
        stage.show();

        bounce.play();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**Synopsis**:
This example demonstrates a simple animation of a bouncing ball. The `TranslateTransition` moves the ball vertically (`setByY`) and reverses its movement (`setAutoReverse(true)`). This creates a natural, dynamic motion, perfect for games or fun visual effects.

---

### Example 4: Scaling Circle
```java
import javafx.animation.*;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.stage.Stage;
import javafx.util.Duration;

public class ScaleAnimation extends Application {
    @Override
    public void start(Stage stage) {
        Circle circle = new Circle(50, Color.GREEN);

        ScaleTransition scale = new ScaleTransition(Duration.seconds(2), circle);
        scale.setFromX(1);
        scale.setToX(2);
        scale.setFromY(1);
        scale.setToY(2);
        scale.setCycleCount(Animation.INDEFINITE);
        scale.setAutoReverse(true);

        Scene scene = new Scene(circle, 400, 400);
        stage.setScene(scene);
        stage.setTitle("Scale Animation");
        stage.show();

        scale.play();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**Synopsis**:
This example uses a `ScaleTransition` to make a circle grow and shrink repeatedly. By scaling both X and Y dimensions, the animation creates a pulsating effect. It’s a useful visual for emphasis or attention-grabbing UI elements.

---

### Example 5: Text Scroller
```java
import javafx.animation.*;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;
import javafx.util.Duration;

public class TextScroller extends Application {
    @Override
    public void start(Stage stage) {
        Label label = new Label("Scrolling Text...");
        label.setStyle("-fx-font-size: 24px;");

        TranslateTransition scroll = new TranslateTransition(Duration.seconds(5), label);
        scroll.setFromX(400);
        scroll.setToX(-200);
        scroll.setCycleCount(Animation.INDEFINITE);

        Scene scene = new Scene(label, 400, 200);
        stage.setScene(scene);
        stage.setTitle("Text Scroller");
        stage.show();

        scroll.play();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**Synopsis**:
This example creates a scrolling text animation using a `TranslateTransition`. The label moves horizontally from right to left, mimicking a marquee effect. It’s great for banners or tickers.

---

### Example 6: Color Changing Rectangle
```java
import javafx.animation.*;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.stage.Stage;
import javafx.util.Duration;

public class ColorAnimation extends Application {
    @Override
    public void start(Stage stage) {
        Rectangle rectangle = new Rectangle(200, 100, Color.RED);

        FillTransition colorChange = new FillTransition(Duration.seconds(2), rectangle, Color.RED, Color.YELLOW);
        colorChange.setCycleCount(Animation.INDEFINITE);
        colorChange.setAutoReverse(true);

        Scene scene = new Scene(rectangle, 400, 400);
        stage.setScene(scene);
        stage.setTitle("Color Animation");
        stage.show();

        colorChange.play();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**Synopsis**:
This example uses a `FillTransition` to animate the color of a rectangle. The color alternates between red and yellow, creating a subtle but engaging effect. This is useful for highlights or attention prompts.

---

### Example 7: Reflective Text
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.effect.Reflection;
import javafx.stage.Stage;

public class ReflectiveText extends Application {
    @Override
    public void start(Stage stage) {
        Label label = new Label("Reflected Text");
        label.setStyle("-fx-font-size: 36px;");

        Reflection reflection = new Reflection();
        label.setEffect(reflection);

        Scene scene = new Scene(label, 400, 200);
        stage.setScene(scene);
        stage.setTitle("Reflection Effect");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**Synopsis**:
This example applies a `Reflection` effect to a text label, giving it a mirrored look. The effect is purely visual and doesn’t require animation, making it a simple but striking addition to any interface.

---

Let me know if you'd like additional examples to complete the list or further enhancements!
