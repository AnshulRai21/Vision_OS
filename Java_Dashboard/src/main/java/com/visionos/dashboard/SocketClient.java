package com.visionos.dashboard;

import javafx.application.Platform;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Consumer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Connects to the Python_AI socket server and streams newline-delimited JSON events. */
public class SocketClient {
    private static final Pattern TYPE_PATTERN = Pattern.compile("\"type\"\\s*:\\s*\"([^\"]*)\"");
    private static final Pattern STRING_FIELD_PATTERN = Pattern.compile("\"([^\"]+)\"\\s*:\\s*\"([^\"]*)\"");
    private static final Pattern NUMBER_FIELD_PATTERN = Pattern.compile("\"([^\"]+)\"\\s*:\\s*([0-9]+(?:\\.[0-9]+)?)");
    private final String host;
    private final int port;
    private final ExecutorService executor = Executors.newSingleThreadExecutor(r -> {
        Thread thread = new Thread(r, "visionos-dashboard-socket");
        thread.setDaemon(true);
        return thread;
    });

    public SocketClient(String host, int port) {
        this.host = host;
        this.port = port;
    }

    /** Begin a background connection attempt. The UI remains usable if Python is not running yet. */
    public void connect(Consumer<DashboardEvent> eventConsumer, Consumer<String> logConsumer) {
        executor.submit(() -> {
            log(logConsumer, "Connecting to Python AI core at " + host + ":" + port + "...");
            try (Socket socket = new Socket(host, port);
                 BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8))) {
                log(logConsumer, "Connected to Python AI core.");
                String line;
                while ((line = reader.readLine()) != null) {
                    DashboardEvent event = parseEvent(line);
                    Platform.runLater(() -> eventConsumer.accept(event));
                }
            } catch (IOException ex) {
                log(logConsumer, "Python AI core unavailable: " + ex.getMessage());
            }
        });
    }

    /** Stop the background socket executor when JavaFX exits. */
    public void shutdown() {
        executor.shutdownNow();
    }

    private DashboardEvent parseEvent(String json) {
        String type = extractType(json);
        Map<String, String> fields = new java.util.HashMap<>();
        Matcher stringMatcher = STRING_FIELD_PATTERN.matcher(json);
        while (stringMatcher.find()) {
            fields.put(stringMatcher.group(1), stringMatcher.group(2));
        }
        Matcher numberMatcher = NUMBER_FIELD_PATTERN.matcher(json);
        while (numberMatcher.find()) {
            fields.put(numberMatcher.group(1), numberMatcher.group(2));
        }
        return new DashboardEvent(type, fields, json);
    }

    private String extractType(String json) {
        Matcher matcher = TYPE_PATTERN.matcher(json);
        return matcher.find() ? matcher.group(1) : "UNKNOWN";
    }

    private void log(Consumer<String> logConsumer, String message) {
        String timestamp = LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss"));
        Platform.runLater(() -> logConsumer.accept("[" + timestamp + "] " + message));
    }

    /** Parsed dashboard event with raw JSON retained for troubleshooting. */
    public record DashboardEvent(String type, Map<String, String> fields, String rawJson) { }
}
