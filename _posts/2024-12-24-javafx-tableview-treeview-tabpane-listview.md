---
layout: mcnz/basic-post
author: Cameron McKenzie
title: Advanced JavaFX Controls and Layouts
blurb: Learn how to use TableView, TreeView, TabPane and ListView in JavaFX.
---


# Part 9: Advanced Controls and Layouts

## Introduction to Advanced Controls

JavaFX provides a range of advanced controls that allow developers to create rich and interactive applications. This section covers four powerful controls—`TableView`, `TreeView`, `TabPane`, and `ListView`—and demonstrates how to customize them using cell factories.

---

## 1. **TableView**

The `TableView` is a versatile control used to display tabular data. It’s highly customizable, supporting sorting, filtering, and editable cells.

### Key API Features
- **Columns and Items**:
  - Use `TableColumn` to define individual columns.
  - Populate data using an `ObservableList`.
- **Editable Tables**:
  - Enable table editing with `setEditable(true)` and define editors for specific columns.

### Important Methods
- `setItems(ObservableList<T> items)`: Sets the data source.
- `getColumns()`: Accesses the table's columns.
- `setEditable(boolean value)`: Enables editing of cells.

### Example: Simple TableView
```java
import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.Scene;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.stage.Stage;

public class TableViewExample extends Application {
    public static class Person {
        private final String name;
        private final int age;

        public Person(String name, int age) {
            this.name = name;
            this.age = age;
        }

        public String getName() {
            return name;
        }

        public int getAge() {
            return age;
        }
    }

    @Override
    public void start(Stage stage) {
        TableView<Person> table = new TableView<>();
        table.setEditable(true);

        // Define columns
        TableColumn<Person, String> nameColumn = new TableColumn<>("Name");
        nameColumn.setCellValueFactory(new PropertyValueFactory<>("name"));

        TableColumn<Person, Integer> ageColumn = new TableColumn<>("Age");
        ageColumn.setCellValueFactory(new PropertyValueFactory<>("age"));

        table.getColumns().addAll(nameColumn, ageColumn);

        // Set data
        ObservableList<Person> data = FXCollections.observableArrayList(
                new Person("Alice", 30),
                new Person("Bob", 25)
        );
        table.setItems(data);

        Scene scene = new Scene(table, 400, 300);
        stage.setScene(scene);
        stage.setTitle("TableView Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**When to Use**:
- Display structured data like reports, inventories, or user lists.
- Support sorting, filtering, or inline editing.

---

## 2. **TreeView**

The `TreeView` is a hierarchical control used for displaying parent-child relationships, such as file systems or organizational structures.

### Key API Features
- **TreeItem**:
  - Represents a single node in the hierarchy.
- **Custom Cell Factories**:
  - Customize the appearance and behavior of tree nodes.

### Important Methods
- `setRoot(TreeItem<T> root)`: Sets the root of the tree.
- `setShowRoot(boolean value)`: Shows or hides the root node.

### Example: Simple TreeView
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.TreeItem;
import javafx.scene.control.TreeView;
import javafx.stage.Stage;

public class TreeViewExample extends Application {
    @Override
    public void start(Stage stage) {
        // Root node
        TreeItem<String> root = new TreeItem<>("Root");
        root.setExpanded(true);

        // Child nodes
        TreeItem<String> child1 = new TreeItem<>("Child 1");
        TreeItem<String> child2 = new TreeItem<>("Child 2");

        root.getChildren().addAll(child1, child2);

        TreeView<String> tree = new TreeView<>(root);
        Scene scene = new Scene(tree, 300, 400);

        stage.setScene(scene);
        stage.setTitle("TreeView Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**When to Use**:
- Represent hierarchical data like folder structures or organizational charts.
- Allow expandable and collapsible views.

---

## 3. **TabPane**

The `TabPane` is used to create tabbed interfaces, making it easy to switch between multiple views or sections.

### Key API Features
- **Tabs**:
  - Each tab contains its own content, defined as a `Node`.
- **Closable Tabs**:
  - Enable or disable the ability to close tabs dynamically.

### Important Methods
- `getTabs()`: Accesses the list of tabs.
- `setSide(Side side)`: Places the tabs on the top, bottom, left, or right.

### Example: Simple TabPane
```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.Tab;
import javafx.scene.control.TabPane;
import javafx.stage.Stage;

public class TabPaneExample extends Application {
    @Override
    public void start(Stage stage) {
        TabPane tabPane = new TabPane();

        // Tabs
        Tab tab1 = new Tab("Tab 1", new Label("Content of Tab 1"));
        Tab tab2 = new Tab("Tab 2", new Label("Content of Tab 2"));
        tabPane.getTabs().addAll(tab1, tab2);

        Scene scene = new Scene(tabPane, 400, 300);
        stage.setScene(scene);
        stage.setTitle("TabPane Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**When to Use**:
- Organize content into sections.
- Build dashboards or multi-view interfaces.

---

## 4. **ListView**

The `ListView` is used to display a scrollable list of items, supporting selection and custom rendering.

### Key API Features
- **Selection Models**:
  - Support single or multiple selections.
- **Custom Cell Factories**:
  - Define how items are displayed.

### Important Methods
- `setItems(ObservableList<T> items)`: Sets the data source.
- `getSelectionModel()`: Accesses the selection model.

### Example: Simple ListView
```java
import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.scene.Scene;
import javafx.scene.control.ListView;
import javafx.stage.Stage;

public class ListViewExample extends Application {
    @Override
    public void start(Stage stage) {
        ListView<String> listView = new ListView<>();
        listView.setItems(FXCollections.observableArrayList("Item 1", "Item 2", "Item 3"));

        Scene scene = new Scene(listView, 300, 400);
        stage.setScene(scene);
        stage.setTitle("ListView Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**When to Use**:
- Display simple lists like menus or playlists.
- Support single or multiple item selection.

---

## Exercise: Build a Simple Dashboard

### Requirements
Create a dashboard with:
1. A `TabPane` with at least two tabs.
2. A `TableView` in one tab to display user data.
3. A `ListView` in another tab to display a list of items.

### Solution Code
```java
import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class DashboardExample extends Application {
    public static class Person {
        private final String name;
        private final int age;

        public Person(String name, int age) {
            this.name = name;
            this.age = age;
        }

        public String getName() {
            return name;
        }

        public int getAge() {
            return age;
        }
    }

    @Override
    public void start(Stage stage) {
        // Tab 1: TableView
        TableView<Person> tableView = new TableView<>();
        TableColumn<Person, String> nameColumn = new TableColumn<>("Name");
        nameColumn.setCellValueFactory(new PropertyValueFactory<>("name"));
        TableColumn<Person, Integer> ageColumn = new TableColumn<>("Age");
        ageColumn.setCellValueFactory(new PropertyValueFactory<>("age"));
        tableView.getColumns().addAll(nameColumn, ageColumn);

        ObservableList<Person> data = FXCollections.observableArrayList(
                new Person("Alice", 30),
                new Person("Bob", 25)
        );
        tableView.setItems(data);
        VBox tableBox = new VBox(tableView);

        // Tab 2: ListView
        ListView<String> listView = new ListView<>();
        listView.setItems(FXCollections.observableArrayList("Item 1", "Item 2", "Item 3"));

        // Create Tabs
        TabPane tabPane = new TabPane();
        tabPane.getTabs().addAll(
                new Tab("Users", tableBox),
                new Tab("Items", listView)
        );

        Scene scene = new Scene(tabPane, 600, 400);
        stage.setScene(scene);
        stage.setTitle("Dashboard Example");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

---

This tutorial introduces powerful JavaFX controls and demonstrates their real-world usage in building dynamic and interactive UIs. Let me know if you’d like further refinements or additional examples!
