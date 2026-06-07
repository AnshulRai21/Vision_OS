package com.visionos.dashboard;

import javafx.geometry.Insets;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;

/** Shows high-priority notifications from the Python security layer. */
public class NotificationPanel extends VBox {
    private final Label notification = new Label("No active notifications");

    public NotificationPanel() {
        setSpacing(8);
        setPadding(new Insets(16));
        setStyle("-fx-background-color: #2b1b1b; -fx-background-radius: 12;");
        Label title = new Label("Notifications");
        title.setStyle("-fx-text-fill: #fca5a5; -fx-font-size: 14px;");
        notification.setStyle("-fx-text-fill: white; -fx-font-size: 18px; -fx-font-weight: bold;");
        getChildren().addAll(title, notification);
    }

    public void update(String message) {
        notification.setText(message == null || message.isBlank() ? "No active notifications" : message);
    }
}
