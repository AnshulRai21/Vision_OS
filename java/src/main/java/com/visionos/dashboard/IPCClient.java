package com.visionos.dashboard;

/** Placeholder client for communication with the Python AI core. */
public class IPCClient {
    private boolean connected;

    /** Open a placeholder connection to the AI core. */
    public void connect() {
        connected = true;
    }

    /** Close the placeholder connection to the AI core. */
    public void disconnect() {
        connected = false;
    }

    /** Return whether the dashboard is connected to the AI core. */
    public boolean isConnected() {
        return connected;
    }
}
