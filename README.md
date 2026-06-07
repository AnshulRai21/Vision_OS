# Vision_OS

Vision_OS is a webcam-driven control system that monitors the user and provides a foundation for laptop control without touching the keyboard or mouse. The system combines:

- OpenCV webcam capture
- MediaPipe AI models for Phase 1 face detection
- A Python processing engine
- A JavaFX desktop dashboard

## Repository layout

```text
python/
  requirements.txt        # Python runtime dependencies
  core/main.py            # Python processing engine entry point
java/
  pom.xml                 # Maven JavaFX build configuration
  src/main/java/...       # JavaFX dashboard source
```

## Python processing engine

From the repository root:

```bash
cd python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m core.main
```

For a startup check that does not import webcam dependencies or open a camera, run:

```bash
cd python
python -m core.main --dry-run
```

## Java desktop dashboard

The Java dashboard uses Maven with the OpenJFX Maven plugin. From the repository root:

```bash
cd java
mvn javafx:run
```

Use JDK 21 or newer for the configured Maven build.
