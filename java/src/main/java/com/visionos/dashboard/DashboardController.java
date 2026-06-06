package com.visionos.dashboard;

/** Coordinates dashboard state and AI-core communication. */
public class DashboardController {
    private final IPCClient ipcClient;

    public DashboardController(IPCClient ipcClient) {
        this.ipcClient = ipcClient;
    }

    /** Return a minimal status message for the initial dashboard scaffold. */
    public String getStatusMessage() {
        return ipcClient.isConnected()
                ? "VisionOS AI core connected"
                : "VisionOS dashboard ready";
    }
}
