package com.visionos.dashboard;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

/** JavaFX dashboard for the VisionOS Phase 1 MVP. */
public class Dashboard extends Application {
    private final CameraPanel cameraPanel = new CameraPanel();
    private final GesturePanel gesturePanel = new GesturePanel();
    private final ActivityPanel activityPanel = new ActivityPanel();
    private final NotificationPanel notificationPanel = new NotificationPanel();
    private final Label userStatus = new Label("AWAY");
    private final Label mouseMode = new Label("OFF");
    private SocketClient socketClient;

    @Override
    public void start(Stage stage) {
        socketClient = new SocketClient("127.0.0.1", 9999);

        BorderPane root = new BorderPane();
        root.setPadding(new Insets(20));
        root.setStyle("-fx-background-color: #050816;");
        root.setTop(header());
        root.setCenter(content());
        root.setBottom(notificationPanel);

        stage.setTitle("VisionOS Dashboard");
        stage.setScene(new Scene(root, 980, 680));
        stage.show();

        socketClient.connect(this::handleEvent, activityPanel::append);
    }

    @Override
    public void stop() {
        if (socketClient != null) {
            socketClient.shutdown();
        }
    }

    private VBox header() {
        Label title = new Label("VisionOS Dashboard");
        title.setStyle("-fx-text-fill: white; -fx-font-size: 32px; -fx-font-weight: bold;");
        Label subtitle = new Label("Phase 1 MVP: Touchless Laptop Control");
        subtitle.setStyle("-fx-text-fill: #9ca3af; -fx-font-size: 15px;");
        VBox box = new VBox(4, title, subtitle);
        box.setPadding(new Insets(0, 0, 20, 0));
        return box;
    }

    private GridPane content() {
        GridPane grid = new GridPane();
        grid.setHgap(16);
        grid.setVgap(16);
        VBox presenceCard = statusCard("User Presence", userStatus);
        VBox mouseCard = statusCard("Mouse Mode", mouseMode);
        grid.add(cameraPanel, 0, 0);
        grid.add(gesturePanel, 1, 0);
        grid.add(presenceCard, 0, 1);
        grid.add(mouseCard, 1, 1);
        grid.add(activityPanel, 0, 2, 2, 1);
        return grid;
    }

    private VBox statusCard(String titleText, Label value) {
        Label title = new Label(titleText);
        title.setStyle("-fx-text-fill: #9fb4d8; -fx-font-size: 14px;");
        value.setStyle("-fx-text-fill: white; -fx-font-size: 24px; -fx-font-weight: bold;");
        VBox card = new VBox(8, title, value);
        card.setPadding(new Insets(16));
        card.setStyle("-fx-background-color: #172033; -fx-background-radius: 12;");
        return card;
    }

    private void handleEvent(SocketClient.DashboardEvent event) {
        String type = event.type();
        if ("STATUS".equals(type)) {
            cameraPanel.update(event.fields().get("camera"), event.fields().get("fps"));
            userStatus.setText(event.fields().getOrDefault("user", "AWAY"));
            mouseMode.setText(event.fields().getOrDefault("mouseMode", "OFF"));
        } else if ("GESTURE".equals(type)) {
            gesturePanel.update(event.fields().get("gesture"), event.fields().get("action"));
            activityPanel.append("Gesture: " + event.fields().get("gesture") + " -> " + event.fields().get("action"));
        } else if ("PRESENCE".equals(type)) {
            userStatus.setText(event.fields().getOrDefault("status", "AWAY"));
            activityPanel.append("User Status: " + event.fields().get("status"));
        } else if ("SECURITY".equals(type)) {
            notificationPanel.update(event.fields().get("notification"));
            activityPanel.append("Security: " + event.fields().get("notification"));
        } else {
            activityPanel.append("Event: " + event.rawJson());
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
