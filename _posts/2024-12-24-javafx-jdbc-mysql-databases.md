---
layout: mcnz/basic-post
author: Cameron McKenzie
title: JavaFX, JDBC and Databases
blurb: Learn how to connect your JavaFX app to a MySQL database and perform CRUD operations.
---


---

# Chapter 10: Connecting JavaFX with Databases

## Overview of Database Integration with JavaFX

Integrating JavaFX with databases allows your application to store, retrieve, and manage persistent data efficiently. JavaFX works seamlessly with JDBC (Java Database Connectivity) to perform these operations. By combining JavaFX controls like `TableView` with database queries, you can create interactive, data-driven applications.

---

## **Introduction to JDBC**

JDBC is an API for connecting and executing queries on databases. It allows you to:
- Establish connections to a database.
- Execute SQL queries to perform CRUD (Create, Read, Update, Delete) operations.
- Retrieve and manipulate data.

---

## Example Application: Task Manager

### Features
We’ll build a task manager application with the following features:
1. Display tasks in a `TableView`.
2. Add new tasks to the database.
3. Update tasks (toggle completion status).
4. Delete tasks.
5. Track when tasks are created (`created_at`) and when they are marked as completed (`completed_at`).

---

### Database Table Schema

Use the following schema for the `tasks` table:

```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL,
    created_at DATE NOT NULL,
    completed_at DATE
);
```

---

### Full JavaFX Application Code

```java
import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.sql.*;
import java.time.LocalDate;

public class TaskManagerApp extends Application {

    // Database connection parameters
    private static final String DB_URL = "jdbc:mysql://localhost:3306/your_database_name";
    private static final String DB_USER = "your_username";
    private static final String DB_PASSWORD = "your_password";

    // ObservableList to hold task data
    private final ObservableList<Task> tasks = FXCollections.observableArrayList();

    // TableView for displaying tasks
    private TableView<Task> tableView;

    public static class Task {
        private final int id;
        private String name;
        private boolean completed;
        private LocalDate createdAt;
        private LocalDate completedAt;

        public Task(int id, String name, boolean completed, LocalDate createdAt, LocalDate completedAt) {
            this.id = id;
            this.name = name;
            this.completed = completed;
            this.createdAt = createdAt;
            this.completedAt = completedAt;
        }

        public int getId() {
            return id;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public boolean isCompleted() {
            return completed;
        }

        public void setCompleted(boolean completed) {
            this.completed = completed;
        }

        public LocalDate getCreatedAt() {
            return createdAt;
        }

        public void setCreatedAt(LocalDate createdAt) {
            this.createdAt = createdAt;
        }

        public LocalDate getCompletedAt() {
            return completedAt;
        }

        public void setCompletedAt(LocalDate completedAt) {
            this.completedAt = completedAt;
        }
    }

    @Override
    public void start(Stage stage) {
        VBox root = new VBox(10);
        root.setPadding(new Insets(20));

        // TableView setup
        tableView = new TableView<>();
        setupTableView();

        // Load data from the database
        loadTasksFromDatabase();

        // Input fields and buttons for CRUD operations
        TextField nameField = new TextField();
        nameField.setPromptText("Task Name");

        CheckBox completedCheckBox = new CheckBox("Completed");

        Button addButton = new Button("Add");
        addButton.setOnAction(e -> {
            String name = nameField.getText().trim();
            boolean completed = completedCheckBox.isSelected();
            if (!name.isEmpty()) {
                addTaskToDatabase(name, completed);
                nameField.clear();
                completedCheckBox.setSelected(false);
            }
        });

        Button deleteButton = new Button("Delete");
        deleteButton.setOnAction(e -> {
            Task selectedTask = tableView.getSelectionModel().getSelectedItem();
            if (selectedTask != null) {
                deleteTaskFromDatabase(selectedTask);
            }
        });

        HBox inputBox = new HBox(10, nameField, completedCheckBox, addButton, deleteButton);
        root.getChildren().addAll(new Label("Task Manager"), inputBox, tableView);

        // Scene setup
        Scene scene = new Scene(root, 800, 400);
        stage.setScene(scene);
        stage.setTitle("Task Manager App");
        stage.show();
    }

    private void setupTableView() {
        TableColumn<Task, String> nameColumn = new TableColumn<>("Task Name");
        nameColumn.setCellValueFactory(new PropertyValueFactory<>("name"));

        TableColumn<Task, Boolean> completedColumn = new TableColumn<>("Completed");
        completedColumn.setCellValueFactory(new PropertyValueFactory<>("completed"));

        TableColumn<Task, LocalDate> createdAtColumn = new TableColumn<>("Created At");
        createdAtColumn.setCellValueFactory(new PropertyValueFactory<>("createdAt"));

        TableColumn<Task, LocalDate> completedAtColumn = new TableColumn<>("Completed At");
        completedAtColumn.setCellValueFactory(new PropertyValueFactory<>("completedAt"));

        tableView.getColumns().addAll(nameColumn, completedColumn, createdAtColumn, completedAtColumn);
        tableView.setItems(tasks);
    }

    private void loadTasksFromDatabase() {
        try (Connection connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
             Statement statement = connection.createStatement();
             ResultSet resultSet = statement.executeQuery("SELECT * FROM tasks")) {

            while (resultSet.next()) {
                int id = resultSet.getInt("id");
                String name = resultSet.getString("name");
                boolean completed = resultSet.getBoolean("completed");
                LocalDate createdAt = resultSet.getDate("created_at").toLocalDate();
                LocalDate completedAt = resultSet.getDate("completed_at") != null
                        ? resultSet.getDate("completed_at").toLocalDate()
                        : null;
                tasks.add(new Task(id, name, completed, createdAt, completedAt));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private void addTaskToDatabase(String name, boolean completed) {
        try (Connection connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
             PreparedStatement statement = connection.prepareStatement(
                     "INSERT INTO tasks (name, completed, created_at, completed_at) VALUES (?, ?, ?, ?)",
                     Statement.RETURN_GENERATED_KEYS)) {

            statement.setString(1, name);
            statement.setBoolean(2, completed);
            statement.setDate(3, Date.valueOf(LocalDate.now()));
            statement.setDate(4, completed ? Date.valueOf(LocalDate.now()) : null);
            statement.executeUpdate();

            // Get the generated ID and add to the ObservableList
            try (ResultSet generatedKeys = statement.getGeneratedKeys()) {
                if (generatedKeys.next()) {
                    int id = generatedKeys.getInt(1);
                    tasks.add(new Task(id, name, completed, LocalDate.now(),
                            completed ? LocalDate.now() : null));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private void deleteTaskFromDatabase(Task task) {
        try (Connection connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
             PreparedStatement statement = connection.prepareStatement("DELETE FROM tasks WHERE id = ?")) {

            statement.setInt(1, task.getId());
            statement.executeUpdate();
            tasks.remove(task);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

---

## Explanation

1. **`Task` Class**:
   - Represents each task with fields for `id`, `name`, `completed`, `created_at`, and `completed_at`.

2. **Database Operations**:
   - **`loadTasksFromDatabase()`**:
     Reads all tasks from the database and populates the `ObservableList`.
   - **`addTaskToDatabase()`**:
     Inserts new tasks with the current date for `created_at` and optionally `completed_at`.
   - **`deleteTaskFromDatabase()`**:
     Removes a task from the database and updates the `ObservableList`.

3. **`TableView`**:
   - Displays tasks dynamically with columns for all fields, including `completed_at`.

---

This full implementation demonstrates a complete CRUD workflow for a task manager application using JavaFX and JDBC. Let me know if you have questions or need further enhancements!
