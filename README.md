# TCAS Dataset

**TCAS: A Fine-Grained Surveillance Dataset for Traffic Crash Anticipation**

This repository contains the TCAS (Traffic Crash Anticipation System) dataset, a comprehensive fine-grained surveillance dataset designed for traffic crash anticipation research. The dataset provides annotated video sequences from surveillance cameras to enable the development and evaluation of machine learning models for predicting traffic crashes before they occur.

## Overview

The TCAS dataset addresses the critical challenge of anticipating traffic crashes in real-time surveillance scenarios. Unlike traditional accident detection systems that react after a crash occurs, this dataset enables research on predictive models that can anticipate crashes seconds before they happen, potentially allowing for preventive interventions.

### Key Features

- **Fine-grained annotations**: Frame-level annotations capturing pre-crash behavior and risk indicators
- **Surveillance camera perspective**: Real-world fixed-camera viewpoints typical of traffic monitoring systems
- **Diverse scenarios**: Multiple crash types, weather conditions, and traffic patterns
- **Temporal coverage**: Sequences include both pre-crash and crash moments for comprehensive analysis
- **High-quality labels**: Expert-annotated dangerous situations and crash precursors

## Dataset Statistics

The TCAS dataset includes:

- **Total videos**: TBD
- **Total frames**: TBD
- **Crash categories**: TBD
- **Average sequence length**: TBD
- **Resolution**: TBD
- **Frame rate**: TBD

> **Note**: Please refer to the paper or contact the dataset maintainers for specific statistics.

## Download and Access

### Dataset Request

The TCAS dataset is available for academic research purposes. To obtain access:

1. **Fill out the request form**: Contact the dataset maintainers (see Contact section below)
2. **Provide your affiliation**: Valid academic or research institution email required
3. **Describe your research**: Brief description of intended use
4. **Agree to terms**: Sign the dataset license agreement

### Terms of Use

- The dataset is for **non-commercial research purposes only**
- Users must **cite the original paper** in any publications using this dataset
- **Redistribution is prohibited** without explicit permission
- Users must comply with privacy and ethical guidelines for video data

## Dataset Structure

The dataset is organized as follows:

```
TCAS-dataset/
├── videos/
│   ├── crash/
│   │   ├── video_001.mp4
│   │   ├── video_002.mp4
│   │   └── ...
│   └── normal/
│       ├── video_001.mp4
│       ├── video_002.mp4
│       └── ...
├── annotations/
│   ├── crash/
│   │   ├── video_001.json
│   │   ├── video_002.json
│   │   └── ...
│   └── normal/
│       ├── video_001.json
│       ├── video_002.json
│       └── ...
├── metadata/
│   ├── train_split.txt
│   ├── val_split.txt
│   ├── test_split.txt
│   └── statistics.json
└── README.md
```

### Annotation Format

Annotations are provided in JSON format with the following structure:

```json
{
  "video_id": "video_001",
  "fps": 30,
  "duration": 120,
  "crash_frame": 3450,
  "crash_type": "rear-end",
  "frames": [
    {
      "frame_id": 3400,
      "timestamp": 113.33,
      "risk_level": "medium",
      "vehicles": [
        {
          "vehicle_id": 1,
          "bbox": [x, y, w, h],
          "type": "car",
          "behavior": "normal"
        }
      ]
    }
  ]
}
```

## Usage

### Loading the Dataset

Here's a basic example of how to load and use the TCAS dataset:

```python
import json
import cv2
import os

class TCASDataset:
    def __init__(self, root_dir, split='train'):
        self.root_dir = root_dir
        self.split = split
        self.video_list = self._load_split()
    
    def _load_split(self):
        split_file = os.path.join(self.root_dir, 'metadata', f'{self.split}_split.txt')
        with open(split_file, 'r') as f:
            return [line.strip() for line in f.readlines()]
    
    def load_video(self, video_id):
        video_path = os.path.join(self.root_dir, 'videos', f'{video_id}.mp4')
        return cv2.VideoCapture(video_path)
    
    def load_annotation(self, video_id):
        anno_path = os.path.join(self.root_dir, 'annotations', f'{video_id}.json')
        with open(anno_path, 'r') as f:
            return json.load(f)

# Example usage
dataset = TCASDataset('/path/to/TCAS-dataset', split='train')
```

### Evaluation Metrics

We recommend using the following metrics for crash anticipation:

- **Time-to-Accident (TTA)**: Measure prediction accuracy at different time windows before crash
- **Precision and Recall**: For crash vs. non-crash classification
- **Average Precision (AP)**: For temporal localization of crash moments
- **F1-Score**: Harmonic mean of precision and recall

## Baseline Models

Please refer to the paper for baseline results and model architectures. We encourage researchers to:

1. Use the provided train/val/test splits for fair comparison
2. Report results with standard metrics
3. Submit results to the leaderboard (if available)

## Citation

If you use the TCAS dataset in your research, please cite our paper:

```bibtex
@inproceedings{tcas2025,
  title={TCAS: A Fine-Grained Surveillance Dataset for Traffic Crash Anticipation},
  author={TBD},
  booktitle={TBD},
  year={2025},
  organization={TBD}
}
```

> **Note**: Please refer to the published paper for the complete citation information.

## License

This dataset is released under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

For questions, issues, or dataset requests:

- **Email**: Please use the GitHub issue tracker or check the published paper for contact information
- **Issues**: Please use the GitHub issue tracker for bug reports and feature requests
- **Updates**: Watch this repository for dataset updates and announcements

## Acknowledgments

We thank all contributors and annotators who made this dataset possible.

## Changelog

### Version 1.0.0 (Initial Release)
- Initial public release of the TCAS dataset
- Comprehensive documentation and dataset loader utilities
- Train/val/test splits specifications provided
