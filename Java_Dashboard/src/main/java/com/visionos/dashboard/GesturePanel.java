package com.visionos.dashboard;

import javafx.geometry.Insets;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;

/** Displays the current recognized gesture and mapped OS action. */
public class GesturePanel extends VBox {
    private final Label gestureValue = new Label("NONE");
    private final Label actionValue = new Label("NO_ACTION");

    public GesturePanel() {
        setSpacing(8);
        setPadding(new Insets(16));
        setStyle("-fx-background-color: #172033; -fx-background-radius: 12;");
        Label title = new Label("Current Gesture");
        title.setStyle("-fx-text-fill: #9fb4d8; -fx-font-size: 14px;");
        gestureValue.setStyle("-fx-text-fill: white; -fx-font-size: 28px; -fx-font-weight: bold;");
        actionValue.setStyle("-fx-text-fill: #63e6be; -fx-font-size: 16px;");
        getChildren().addAll(title, gestureValue, actionValue);
    }

    public void update(String gesture, String action) {
        gestureValue.setText(gesture == null ? "NONE" : gesture);
        actionValue.setText(action == null ? "NO_ACTION" : action);
    }
}
