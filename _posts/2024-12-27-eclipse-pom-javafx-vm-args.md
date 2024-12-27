---
layout: mcnz/basic-post
author: Cameron McKenzie
title: JavaFX, Eclipse, POM, VM Args
blurb: Here's how to run JavaFX apps in Eclipse.
---




https://gluonhq.com/products/javafx/

--module-path "C:\javafx-sdk\lib" --add-modules javafx.controls,javafx.graphics,javafx.fxml

```
<dependencies>
    <!-- JavaFX dependencies -->
    <dependency>
        <groupId>org.openjfx</groupId>
        <artifactId>javafx-controls</artifactId>
        <version>23</version>
    </dependency>
    <dependency>
        <groupId>org.openjfx</groupId>
        <artifactId>javafx-fxml</artifactId>
        <version>23}</version>
    </dependency>
</dependencies>
```
