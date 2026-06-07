package com.visionos.dashboard;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;

/** JavaFX application scaffold for the VisionOS desktop dashboard. */
public class VisionOSDashboardApp extends Application {
    @Override
    public void start(Stage stage) {
        DashboardController controller = new DashboardController(new IPCClient());
        Label statusLabel = new Label(controller.getStatusMessage());
        stage.setTitle("VisionOS Dashboard");
        stage.setScene(new Scene(statusLabel, 480, 240));
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
