# TCAS Dataset Format Specification

This document provides detailed specifications for the TCAS dataset format, including file structures, annotation schemas, and data conventions.

## Video Files

### Format and Specifications

- **Container**: MP4 (H.264 encoding)
- **Resolution**: 1920x1080 pixels (Full HD)
- **Frame Rate**: 30 FPS (frames per second)
- **Color Space**: RGB
- **Codec**: H.264/AVC
- **Bitrate**: Variable (avg. 5-10 Mbps)

### Naming Convention

Videos are named using the following pattern:
```
{category}_{sequence_id}.mp4
```

Where:
- `category`: Either "crash" or "normal"
- `sequence_id`: Zero-padded 3-digit identifier (e.g., 001, 002, 123)

Examples:
- `crash_001.mp4`
- `normal_045.mp4`

## Annotation Files

Annotations are stored in JSON format with one file per video.

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["video_id", "fps", "duration", "category"],
  "properties": {
    "video_id": {
      "type": "string",
      "description": "Unique identifier for the video"
    },
    "fps": {
      "type": "integer",
      "description": "Frames per second of the video"
    },
    "duration": {
      "type": "number",
      "description": "Duration of video in seconds"
    },
    "category": {
      "type": "string",
      "enum": ["crash", "normal"],
      "description": "Category of the video"
    },
    "crash_frame": {
      "type": "integer",
      "description": "Frame number where crash occurs (only for crash videos)"
    },
    "crash_type": {
      "type": "string",
      "enum": ["rear-end", "side-impact", "head-on", "pedestrian", "vehicle-object"],
      "description": "Type of crash (only for crash videos)"
    },
    "weather": {
      "type": "string",
      "enum": ["clear", "rainy", "foggy", "snowy"],
      "description": "Weather condition during recording"
    },
    "time_of_day": {
      "type": "string",
      "enum": ["day", "night", "dawn", "dusk"],
      "description": "Time of day during recording"
    },
    "camera_info": {
      "type": "object",
      "properties": {
        "height": {
          "type": "number",
          "description": "Camera height in meters"
        },
        "angle": {
          "type": "number",
          "description": "Camera angle in degrees"
        },
        "location_type": {
          "type": "string",
          "enum": ["intersection", "highway", "urban", "rural"],
          "description": "Type of location"
        }
      }
    },
    "frames": {
      "type": "array",
      "description": "Frame-level annotations",
      "items": {
        "type": "object",
        "required": ["frame_id", "timestamp"],
        "properties": {
          "frame_id": {
            "type": "integer",
            "description": "Frame number (0-indexed)"
          },
          "timestamp": {
            "type": "number",
            "description": "Timestamp in seconds"
          },
          "risk_level": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"],
            "description": "Assessed risk level at this frame"
          },
          "vehicles": {
            "type": "array",
            "description": "Vehicle detections in frame",
            "items": {
              "type": "object",
              "properties": {
                "vehicle_id": {
                  "type": "integer",
                  "description": "Unique vehicle identifier within video"
                },
                "bbox": {
                  "type": "array",
                  "items": {"type": "number"},
                  "minItems": 4,
                  "maxItems": 4,
                  "description": "Bounding box [x, y, width, height] in pixels"
                },
                "type": {
                  "type": "string",
                  "enum": ["car", "truck", "bus", "motorcycle", "bicycle"],
                  "description": "Vehicle type"
                },
                "behavior": {
                  "type": "string",
                  "enum": ["normal", "aggressive", "erratic", "stopping", "turning"],
                  "description": "Vehicle behavior classification"
                },
                "speed": {
                  "type": "number",
                  "description": "Estimated speed in km/h (optional)"
                }
              }
            }
          },
          "pedestrians": {
            "type": "array",
            "description": "Pedestrian detections in frame",
            "items": {
              "type": "object",
              "properties": {
                "pedestrian_id": {
                  "type": "integer",
                  "description": "Unique pedestrian identifier"
                },
                "bbox": {
                  "type": "array",
                  "items": {"type": "number"},
                  "minItems": 4,
                  "maxItems": 4,
                  "description": "Bounding box [x, y, width, height]"
                },
                "action": {
                  "type": "string",
                  "enum": ["standing", "walking", "running", "crossing"],
                  "description": "Pedestrian action"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Example Annotation

```json
{
  "video_id": "crash_001",
  "fps": 30,
  "duration": 120.5,
  "category": "crash",
  "crash_frame": 3450,
  "crash_type": "rear-end",
  "weather": "clear",
  "time_of_day": "day",
  "camera_info": {
    "height": 8.5,
    "angle": 45,
    "location_type": "intersection"
  },
  "frames": [
    {
      "frame_id": 3400,
      "timestamp": 113.33,
      "risk_level": "medium",
      "vehicles": [
        {
          "vehicle_id": 1,
          "bbox": [450, 320, 180, 120],
          "type": "car",
          "behavior": "normal",
          "speed": 45.2
        },
        {
          "vehicle_id": 2,
          "bbox": [450, 180, 190, 125],
          "type": "car",
          "behavior": "aggressive",
          "speed": 68.5
        }
      ]
    },
    {
      "frame_id": 3450,
      "timestamp": 115.0,
      "risk_level": "critical",
      "vehicles": [
        {
          "vehicle_id": 1,
          "bbox": [455, 325, 180, 120],
          "type": "car",
          "behavior": "stopping",
          "speed": 10.5
        },
        {
          "vehicle_id": 2,
          "bbox": [452, 245, 190, 125],
          "type": "car",
          "behavior": "erratic",
          "speed": 65.0
        }
      ]
    }
  ]
}
```

## Metadata Files

### Split Files

Train/validation/test splits are provided in plain text files:

- `train_split.txt`
- `val_split.txt`
- `test_split.txt`

Format: One video ID per line (without extension)
```
crash_001
crash_002
normal_001
normal_045
```

### Statistics File

`statistics.json` provides dataset-wide statistics:

```json
{
  "total_videos": 1500,
  "total_frames": 4500000,
  "crash_videos": 750,
  "normal_videos": 750,
  "crash_types": {
    "rear-end": 320,
    "side-impact": 215,
    "head-on": 110,
    "pedestrian": 80,
    "vehicle-object": 25
  },
  "weather_distribution": {
    "clear": 1050,
    "rainy": 280,
    "foggy": 120,
    "snowy": 50
  },
  "avg_duration": 90.5,
  "total_duration_hours": 37.5
}
```

## Coordinate System

- **Origin**: Top-left corner of the image
- **X-axis**: Increases to the right
- **Y-axis**: Increases downward
- **Bounding Box Format**: [x, y, width, height]
  - `x, y`: Top-left corner coordinates
  - `width, height`: Box dimensions in pixels

## Risk Level Definitions

- **Low**: Normal traffic flow, no immediate threats
- **Medium**: Potentially dangerous situations developing (e.g., close following, lane changes)
- **High**: Dangerous situations present (e.g., aggressive driving, near-misses)
- **Critical**: Imminent crash or crash occurring

## Version History

- **v1.0**: Initial release with basic annotations
- Future versions may include additional annotation types or refined labels

## Notes

- Not all frames are annotated; typically, annotations are provided at key moments
- Frame IDs are 0-indexed
- Timestamps are relative to video start (0.0 seconds)
- Some optional fields may be missing in certain annotations
