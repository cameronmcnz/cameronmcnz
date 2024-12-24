---
layout: mcnz/basic-post
author: Cameron McKenzie
title: JavaFX TODO List Challenge
blurb: Want to put your skills to the test? Create a feature-rich TODO list!
---



### Assignment: Build Your Own JavaFX TODO App

**Objective**: Create a functional and visually appealing TODO application in JavaFX that allows users to manage their tasks effectively.

---

### **What You Will Build**

You will create a JavaFX application that provides the following features:
1. **Add Tasks**: Users can add new tasks to a list.
2. **Mark Tasks as Completed**: Users can toggle the completion status of a task.
3. **Delete Tasks**: Users can remove tasks from the list.
4. **Task Details**: Optional: Users can click on a task to view or edit additional details about it (e.g., due date, priority).
5. **Persistent Storage**: Optional: Save tasks to a file so that they persist when the application is closed and reopened.

---

### **Features Your App Should Have**

1. **User Interface**:
   - A text input field for entering new tasks.
   - Buttons to add, mark as completed, undo, or delete tasks.
   - A list that displays all tasks dynamically.

2. **Task Representation**:
   - Each task should display:
     - The task name.
     - Completion status (e.g., strikethrough text or a checkbox).
   - Include actions to "Complete/Undo" and "Delete" tasks.

3. **Styling**:
   - Use JavaFX styles to differentiate completed tasks visually (e.g., grayed-out text with strikethrough).

---

### **Suggested Classes and Properties**

To manage your TODO list effectively, you will need the following:

#### **1. Supporting Class for Tasks**
Define a `Task` class to represent a single TODO item.

**Suggested Properties**:
- `StringProperty name`: Stores the task's name.
- `BooleanProperty isCompleted`: Tracks whether the task is completed.
- (Optional) `StringProperty details`: Additional details about the task (e.g., due date or priority).

**Suggested Methods**:
- **Constructor**: Initializes the task with a name and default values for other properties.
  ```java
  public Task(String name) { ... }
  ```
- **Getters and Setters**: Provide access to the properties.
  ```java
  public String getName();
  public void setName(String name);
  public boolean isCompleted();
  public void setCompleted(boolean isCompleted);
  ```
- (Optional) **toString**: Return a user-friendly representation of the task.
  ```java
  public String toString() { ... }
  ```

---

#### **2. Managing the Task List**
Use an `ObservableList<Task>` to store tasks and dynamically update the UI when changes occur.

**Suggested Methods**:
- **addTask(String name)**:
  - Adds a new task to the list.
  - **Parameter**: `String name` - The name of the task to add.

- **deleteTask(Task task)**:
  - Removes a task from the list.
  - **Parameter**: `Task task` - The task to delete.

- **toggleTaskCompletion(Task task)**:
  - Toggles the completion status of a task.
  - **Parameter**: `Task task` - The task to update.

---

### **Hints for UI Design**

1. **Input Section**:
   - Use a `TextField` for entering new tasks and a `Button` to add them to the list.

2. **Task Display**:
   - Use a `ListView<Task>` for displaying tasks.
   - Implement a custom cell factory to render tasks with the "Complete/Undo" and "Delete" buttons.

3. **Dynamic Updates**:
   - Use property bindings to dynamically update the UI when task properties change.

4. **Styling**:
   - Use CSS-like styles for completed tasks:
     ```css
     -fx-text-fill: gray;
     -fx-strikethrough: true;
     ```

---

### **Challenge Features**

1. **Task Details View**:
   - Create a modal dialog that allows users to view or edit task details, such as due dates or priority levels.

2. **Task Filtering**:
   - Add options to filter tasks (e.g., show only incomplete tasks or tasks with a specific priority).

3. **Persistence**:
   - Save the task list to a file (e.g., JSON or plain text) and reload it when the application starts.

---

### **Encouragement**

- **Think Creatively**:
  - Experiment with UI layouts (e.g., add tabs or multiple views for organizing tasks).
- **Explore JavaFX Properties**:
  - Learn how `StringProperty` and `BooleanProperty` work and how they simplify UI updates.
- **Adapt the Suggestions**:
  - Use the suggested methods and properties as a guide, but don’t feel obligated to follow them exactly.

---

### **What You’ll Learn**

- How to use JavaFX properties and bindings to create dynamic UIs.
- How to work with `ObservableList` to manage and display collections.
- How to implement custom cell factories for `ListView`.
- Optional: How to persist data for application reusability.

---

### **Submission Requirements**

1. The full JavaFX application code.
2. Screenshots of the app in action, showing:
   - Adding, completing, and deleting tasks.
   - (Optional) Task details view or filtering.
3. A short description of how your app works and the decisions you made during development.

---


Here is the completed code:

```
import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class ToDoApp extends Application {

    // Observable list to store the TODO items
    private final ObservableList<ToDoItem> toDoList = FXCollections.observableArrayList();

    public static class ToDoItem {
        private String name;
        private boolean isCompleted;

        public ToDoItem(String name, boolean isCompleted) {
            this.name = name;
            this.isCompleted = isCompleted;
        }

        public String getName() {
            return name;
        }

        public boolean isCompleted() {
            return isCompleted;
        }

        public void setName(String name) {
            this.name = name;
        }

        public void setCompleted(boolean completed) {
            isCompleted = completed;
        }
    }

    @Override
    public void start(Stage stage) {
        VBox root = new VBox(10);
        root.setPadding(new Insets(20));

        // Input field for new TODO items
        TextField inputField = new TextField();
        inputField.setPromptText("Enter a task");

        // Add button
        Button addButton = new Button("Add");
        addButton.setOnAction(e -> {
            String task = inputField.getText().trim();
            if (!task.isEmpty()) {
                toDoList.add(new ToDoItem(task, false));
                inputField.clear();
            }
        });

        // List view to display TODO items
        ListView<ToDoItem> listView = new ListView<>(toDoList);
        listView.setCellFactory(lv -> new ToDoCell());

        // Add the input field, button, and list to the layout
        HBox inputBox = new HBox(10, inputField, addButton);
        root.getChildren().addAll(new Label("Things To Do"), inputBox, listView);

        // Scene setup
        Scene scene = new Scene(root, 400, 400);
        stage.setScene(scene);
        stage.setTitle("TODO App");
        stage.show();
    }

    private static class ToDoCell extends ListCell<ToDoItem> {
        @Override
        protected void updateItem(ToDoItem item, boolean empty) {
            super.updateItem(item, empty);
            if (empty || item == null) {
                setText(null);
                setGraphic(null);
            } else {
                HBox cellBox = new HBox(10);
                Label nameLabel = new Label(item.getName());
                nameLabel.setStyle(item.isCompleted() ? "-fx-text-fill: gray; -fx-strikethrough: true;" : "-fx-text-fill: black;");

                // Complete/Undo button
                Button completeButton = new Button(item.isCompleted() ? "Undo" : "Complete");
                completeButton.setOnAction(e -> {
                    item.setCompleted(!item.isCompleted());
                    nameLabel.setStyle(item.isCompleted() ? "-fx-text-fill: gray; -fx-strikethrough: true;" : "-fx-text-fill: black;");
                    completeButton.setText(item.isCompleted() ? "Undo" : "Complete");
                });

                // Delete button
                Button deleteButton = new Button("Delete");
                deleteButton.setOnAction(e -> getListView().getItems().remove(item));

                cellBox.getChildren().addAll(nameLabel, completeButton, deleteButton);
                setGraphic(cellBox);
            }
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```
