package com.visionos.dashboard;

import javafx.geometry.Insets;
import javafx.scene.control.TextArea;
import javafx.scene.layout.VBox;

/** Recent activity log panel for gestures, presence changes, and security events. */
public class ActivityPanel extends VBox {
    private final TextArea logs = new TextArea();

    public ActivityPanel() {
        setSpacing(8);
        setPadding(new Insets(16));
        setStyle("-fx-background-color: #111827; -fx-background-radius: 12;");
        logs.setEditable(false);
        logs.setWrapText(true);
        logs.setPrefRowCount(12);
        logs.setStyle("-fx-control-inner-background: #0b1220; -fx-text-fill: #e5e7eb;");
        getChildren().add(logs);
    }

    public void append(String line) {
        logs.appendText(line + System.lineSeparator());
    }
}
