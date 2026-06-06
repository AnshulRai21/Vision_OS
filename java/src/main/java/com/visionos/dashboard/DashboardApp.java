package com.visionos.dashboard;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

/** JavaFX desktop dashboard entry point for Vision_OS. */
public class DashboardApp extends Application {
    @Override
    public void start(Stage stage) {
        Label title = new Label("Vision_OS Dashboard");
        title.setStyle("-fx-font-size: 24px; -fx-font-weight: bold;");

        Label status = new Label("Phase 1: Python webcam and MediaPipe face detection engine.");

        VBox root = new VBox(12, title, status);
        root.setPadding(new Insets(24));

        stage.setTitle("Vision_OS Dashboard");
        stage.setScene(new Scene(root, 640, 360));
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
