# TCAS Dataset Examples

This directory contains example scripts and notebooks for working with the TCAS dataset.

## Quick Start

### 1. Basic Data Loading

```python
from tcas_loader import TCASDataset

# Load training data
dataset = TCASDataset('/path/to/TCAS-dataset', split='train')

# Get a sample
sample = dataset[0]
print(f"Video ID: {sample['video_id']}")
print(f"Frames shape: {sample['frames'].shape}")
```

### 2. Iterating Through Dataset

```python
from tcas_loader import TCASDataset

dataset = TCASDataset('/path/to/TCAS-dataset', split='train')

for i in range(len(dataset)):
    sample = dataset[i]
    video_id = sample['video_id']
    annotation = sample['annotation']
    
    if annotation['category'] == 'crash':
        crash_frame = annotation['crash_frame']
        crash_type = annotation['crash_type']
        print(f"{video_id}: {crash_type} crash at frame {crash_frame}")
```

### 3. Working with Specific Frames

```python
from tcas_loader import TCASDataset

dataset = TCASDataset('/path/to/TCAS-dataset', split='train')
video_id = 'crash_001'

# Get frame annotation
frame_anno = dataset.get_frame_annotation(video_id, frame_id=3400)

if frame_anno:
    print(f"Risk level: {frame_anno['risk_level']}")
    print(f"Number of vehicles: {len(frame_anno.get('vehicles', []))}")
```

### 4. Visualizing Annotations

```python
from tcas_loader import TCASDataset, visualize_frame

dataset = TCASDataset('/path/to/TCAS-dataset', split='train')

# Load a video
sample = dataset[0]
frames = sample['frames']
annotation = sample['annotation']

# Visualize a specific frame
if annotation['frames']:
    frame_anno = annotation['frames'][0]
    frame_id = frame_anno['frame_id']
    visualize_frame(frames[frame_id], frame_anno, save_path='output.png')
```

### 5. Computing Time to Accident

```python
from tcas_loader import TCASDataset, compute_time_to_accident

dataset = TCASDataset('/path/to/TCAS-dataset', split='train')
video_id = 'crash_001'

annotation = dataset.load_annotation(video_id)
crash_frame = annotation['crash_frame']
fps = annotation['fps']

# Check multiple time points
for current_frame in [crash_frame - 150, crash_frame - 90, crash_frame - 30]:
    tta = compute_time_to_accident(crash_frame, current_frame, fps)
    print(f"Frame {current_frame}: TTA = {tta:.2f} seconds")
```

### 6. Filtering Videos by Type

```python
from tcas_loader import TCASDataset

dataset = TCASDataset('/path/to/TCAS-dataset', split='train')

# Find all rear-end crashes
rear_end_crashes = []
for video_id in dataset.video_ids:
    annotation = dataset.load_annotation(video_id)
    if annotation.get('crash_type') == 'rear-end':
        rear_end_crashes.append(video_id)

print(f"Found {len(rear_end_crashes)} rear-end crashes")
```

### 7. Creating Custom DataLoader (PyTorch)

```python
import torch
from torch.utils.data import Dataset, DataLoader
from tcas_loader import TCASDataset
import numpy as np

class TCASPyTorchDataset(Dataset):
    def __init__(self, root_dir, split='train', transform=None):
        self.tcas_dataset = TCASDataset(root_dir, split)
        self.transform = transform
    
    def __len__(self):
        return len(self.tcas_dataset)
    
    def __getitem__(self, idx):
        sample = self.tcas_dataset[idx]
        
        # Convert frames to tensor
        frames = torch.from_numpy(sample['frames']).float()
        frames = frames.permute(0, 3, 1, 2)  # (T, H, W, C) -> (T, C, H, W)
        
        # Create label (1 for crash, 0 for normal)
        label = 1 if sample['annotation']['category'] == 'crash' else 0
        
        if self.transform:
            frames = self.transform(frames)
        
        return frames, label

# Usage
train_dataset = TCASPyTorchDataset('/path/to/TCAS-dataset', split='train')
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)

for batch_frames, batch_labels in train_loader:
    # Train your model
    pass
```

### 8. Extracting Dataset Statistics

```python
from tcas_loader import TCASDataset

dataset = TCASDataset('/path/to/TCAS-dataset', split='train')

# Load statistics
stats = dataset.get_statistics()

print("Dataset Statistics:")
print(f"Total videos: {stats['total_videos']}")
print(f"Crash videos: {stats['crash_videos']}")
print(f"Normal videos: {stats['normal_videos']}")

print("\nCrash type distribution:")
for crash_type, count in stats['crash_types'].items():
    print(f"  {crash_type}: {count}")

print("\nWeather distribution:")
for weather, count in stats['weather_distribution'].items():
    print(f"  {weather}: {count}")
```

## Advanced Examples

For more advanced examples including:
- Training baseline models
- Implementing crash anticipation algorithms
- Evaluation metrics computation
- Temporal action localization

Please refer to the full examples in the repository or contact the maintainers.

## Requirements

```bash
pip install numpy opencv-python matplotlib torch torchvision
```

## Support

If you encounter any issues with these examples, please open an issue on GitHub or contact the maintainers.
