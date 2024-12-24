---
layout: mcnz/basic-post
author: Cameron McKenzie
title: JavaFX Packaging and Deployment
blurb: Learn how to package and deploy your JavaFX applications.
---


# Part 11: Packaging and Deployment

After developing a JavaFX application, the next step is to package and deploy it. Packaging ensures your application is ready for distribution, while deployment enables users to easily install and run it. This chapter covers how to export your JavaFX app as a JAR file and how to package it as a standalone executable using `jlink`.

---

## Exporting a JavaFX App: Creating a JAR File with Dependencies

### Why Package as a JAR?
- A **JAR (Java Archive)** file bundles all the code, resources, and libraries into a single distributable file.
- It simplifies sharing and deployment.

### Steps to Create a JAR File
1. **Set Up Your Project**:
   Ensure your JavaFX application and dependencies are properly configured.

2. **Generate the JAR**:
   Use your IDE or the command line to create a JAR file.

#### Example: Using IntelliJ IDEA
1. Go to **File > Project Structure > Artifacts**.
2. Click **+ > JAR > From modules with dependencies**.
3. Select your main class and click **OK**.
4. Click **Build > Build Artifacts > Build**.

#### Example: Using Command Line
If you’re using Maven or Gradle, you can package your application with the following:

**For Maven**:
```bash
mvn clean package
```

**For Gradle**:
```bash
gradle build
```

**For Manual JAR Creation**:
```bash
javac -d out src/*.java
jar cfe App.jar Main -C out .
```

### Running the JAR
Run the JAR file with the following command:
```bash
java -jar App.jar
```

---

## Using `jlink`: Packaging JavaFX Apps as Standalone Executables

### What is `jlink`?
`jlink` is a tool included in the JDK that creates custom runtime images. It packages the JavaFX runtime with your application, allowing users to run it without separately installing Java.

---

### Steps to Package a JavaFX App with `jlink`

1. **Install JDK with JavaFX Support**:
   Ensure you’re using a JDK that includes JavaFX (e.g., OpenJFX or ZuluFX).

2. **Compile the Application**:
   Compile your JavaFX application into `.class` files.

3. **Create a Custom Runtime Image**:
   Use `jlink` to bundle your application with the necessary Java modules.

#### Example:
Assuming your application is in a JAR file (`App.jar`) and you have a `module-info.java` file, run the following:

```bash
jlink --module-path $JAVA_HOME/jmods:libs \
      --add-modules javafx.controls,javafx.fxml,your.module.name \
      --output MyApp \
      --launcher MyLauncher=your.module.name/your.main.class \
      --compress=2
```

- `--module-path`: Path to the JDK `jmods` directory and your dependencies.
- `--add-modules`: JavaFX modules and your application module.
- `--output`: Directory for the output image.
- `--launcher`: Creates a script to run your app.

4. **Run the Standalone Application**:
Navigate to the output directory and run the application:
```bash
./MyApp/bin/MyLauncher
```

5. **Distribute the Application**:
Share the entire output directory with users. It includes your app, a custom JRE, and launch scripts.

---

## Exercise: Package and Run Your App as a Desktop Application

### Task
1. Package your JavaFX application as a runnable JAR file.
2. Use `jlink` to create a custom runtime image and package it as a standalone desktop application.

---

### Steps for the Exercise

1. **Create the JAR File**:
   Follow the steps in the "Exporting a JavaFX App" section to create the JAR file.

2. **Use `jlink`**:
   Create a standalone executable for your application.

3. **Test the Application**:
   - Test the standalone executable on your local machine.
   - Verify that it runs without requiring any external dependencies.

4. **Deliver the Application**:
   - Share the JAR or runtime image with others.
   - Include documentation or instructions on how to run the application.

---

### Solution: Packaging the Task Manager Application

Here’s a summary of how to package the Task Manager app built in the previous chapters:

1. **Export as a JAR**:
   - Compile the application using an IDE or `javac`.
   - Create a runnable JAR with all dependencies.

2. **Use `jlink`**:
   - Run `jlink` to package the application with JavaFX modules and a custom runtime.

**Command**:
```bash
jlink --module-path $JAVA_HOME/jmods:libs \
      --add-modules javafx.controls,javafx.fxml,task.manager.app \
      --output TaskManagerApp \
      --launcher TaskManager=task.manager.app/Main \
      --compress=2
```

3. **Run the Application**:
   ```bash
   ./TaskManagerApp/bin/TaskManager
   ```

4. **Test and Share**:
   Test the app on different machines and share it as a self-contained package.

---

### Why Use `jlink`?
- Simplifies deployment: Users don’t need to install Java.
- Customizes the runtime: Includes only the necessary Java modules, reducing the application size.
- Creates a professional-grade, standalone application.

---



With this chapter, you’ve learned how to package and deploy your JavaFX applications. These skills ensure that your apps are ready for distribution, whether as JAR files or standalone executables. 
