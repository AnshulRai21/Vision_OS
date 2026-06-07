package com.visionos.dashboard;

import javafx.geometry.Insets;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;

/** Camera status card. The live OpenCV window is rendered by Python in the MVP. */
public class CameraPanel extends VBox {
    private final Label cameraStatus = new Label("WAITING");
    private final Label fpsStatus = new Label("FPS: --");

    public CameraPanel() {
        setSpacing(8);
        setPadding(new Insets(16));
        setStyle("-fx-background-color: #172033; -fx-background-radius: 12;");
        Label title = new Label("Camera Status");
        title.setStyle("-fx-text-fill: #9fb4d8; -fx-font-size: 14px;");
        cameraStatus.setStyle("-fx-text-fill: white; -fx-font-size: 24px; -fx-font-weight: bold;");
        fpsStatus.setStyle("-fx-text-fill: #93c5fd; -fx-font-size: 16px;");
        getChildren().addAll(title, cameraStatus, fpsStatus);
    }

    public void update(String status, String fps) {
        cameraStatus.setText(status == null ? "WAITING" : status);
        fpsStatus.setText("FPS: " + (fps == null ? "--" : fps));
    }
}
