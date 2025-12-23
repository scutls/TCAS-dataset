"""
TCAS Dataset Loader

This module provides utilities for loading and working with the TCAS dataset.
"""

import json
import os
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np


class TCASDataset:
    """
    TCAS Dataset loader for traffic crash anticipation.
    
    Args:
        root_dir (str): Root directory of the TCAS dataset
        split (str): One of 'train', 'val', or 'test'
        transform (callable, optional): Optional transform to apply to frames
    """
    
    def __init__(self, root_dir: str, split: str = 'train', transform=None):
        self.root_dir = root_dir
        self.split = split
        self.transform = transform
        
        # Load video list for this split
        self.video_ids = self._load_split()
        
        # Cache for annotations
        self._annotation_cache = {}
        
    def _load_split(self) -> List[str]:
        """Load the list of video IDs for the current split."""
        split_file = os.path.join(self.root_dir, 'metadata', f'{self.split}_split.txt')
        
        if not os.path.exists(split_file):
            raise FileNotFoundError(f"Split file not found: {split_file}")
        
        with open(split_file, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    
    def __len__(self) -> int:
        """Return the number of videos in this split."""
        return len(self.video_ids)
    
    def __getitem__(self, idx: int) -> Dict:
        """
        Get a video and its annotations by index.
        
        Args:
            idx (int): Index of the video
            
        Returns:
            dict: Dictionary containing video frames and annotations
        """
        video_id = self.video_ids[idx]
        
        # Load video
        frames = self.load_video_frames(video_id)
        
        # Load annotations
        annotation = self.load_annotation(video_id)
        
        return {
            'video_id': video_id,
            'frames': frames,
            'annotation': annotation
        }
    
    def load_video_frames(self, video_id: str) -> np.ndarray:
        """
        Load all frames from a video.
        
        Args:
            video_id (str): Video identifier
            
        Returns:
            np.ndarray: Array of frames with shape (num_frames, height, width, channels)
        """
        # Determine video path
        if video_id.startswith('crash_'):
            video_path = os.path.join(self.root_dir, 'videos', 'crash', f'{video_id}.mp4')
        else:
            video_path = os.path.join(self.root_dir, 'videos', 'normal', f'{video_id}.mp4')
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Load video
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Apply transform if provided
            if self.transform:
                frame = self.transform(frame)
            
            frames.append(frame)
        
        cap.release()
        
        return np.array(frames)
    
    def load_annotation(self, video_id: str) -> Dict:
        """
        Load annotation for a video.
        
        Args:
            video_id (str): Video identifier
            
        Returns:
            dict: Annotation dictionary
        """
        # Check cache
        if video_id in self._annotation_cache:
            return self._annotation_cache[video_id]
        
        # Determine annotation path
        if video_id.startswith('crash_'):
            anno_path = os.path.join(self.root_dir, 'annotations', 'crash', f'{video_id}.json')
        else:
            anno_path = os.path.join(self.root_dir, 'annotations', 'normal', f'{video_id}.json')
        
        if not os.path.exists(anno_path):
            raise FileNotFoundError(f"Annotation file not found: {anno_path}")
        
        with open(anno_path, 'r') as f:
            annotation = json.load(f)
        
        # Cache annotation
        self._annotation_cache[video_id] = annotation
        
        return annotation
    
    def get_frame_annotation(self, video_id: str, frame_id: int) -> Optional[Dict]:
        """
        Get annotation for a specific frame.
        
        Args:
            video_id (str): Video identifier
            frame_id (int): Frame number
            
        Returns:
            dict or None: Frame annotation if available, None otherwise
        """
        annotation = self.load_annotation(video_id)
        
        for frame_anno in annotation.get('frames', []):
            if frame_anno['frame_id'] == frame_id:
                return frame_anno
        
        return None
    
    def is_crash_video(self, video_id: str) -> bool:
        """Check if a video contains a crash."""
        annotation = self.load_annotation(video_id)
        return annotation.get('category') == 'crash'
    
    def get_crash_frame(self, video_id: str) -> Optional[int]:
        """
        Get the frame number where crash occurs.
        
        Args:
            video_id (str): Video identifier
            
        Returns:
            int or None: Crash frame number if video contains crash, None otherwise
        """
        annotation = self.load_annotation(video_id)
        return annotation.get('crash_frame')
    
    def get_statistics(self) -> Dict:
        """
        Load dataset statistics.
        
        Returns:
            dict: Statistics dictionary
        """
        stats_path = os.path.join(self.root_dir, 'metadata', 'statistics.json')
        
        if not os.path.exists(stats_path):
            raise FileNotFoundError(f"Statistics file not found: {stats_path}")
        
        with open(stats_path, 'r') as f:
            return json.load(f)


def visualize_frame(frame: np.ndarray, annotation: Dict, save_path: Optional[str] = None):
    """
    Visualize a frame with its annotations.
    
    Args:
        frame (np.ndarray): Frame image
        annotation (dict): Frame annotation
        save_path (str, optional): Path to save the visualization
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    
    fig, ax = plt.subplots(1, figsize=(12, 8))
    ax.imshow(frame)
    
    # Draw vehicle bounding boxes
    for vehicle in annotation.get('vehicles', []):
        bbox = vehicle['bbox']
        x, y, w, h = bbox
        
        # Color based on behavior
        behavior = vehicle.get('behavior', 'normal')
        color_map = {
            'normal': 'green',
            'aggressive': 'orange',
            'erratic': 'red',
            'stopping': 'yellow',
            'turning': 'blue'
        }
        color = color_map.get(behavior, 'green')
        
        rect = patches.Rectangle((x, y), w, h, linewidth=2, 
                                 edgecolor=color, facecolor='none')
        ax.add_patch(rect)
        
        # Add label
        label = f"{vehicle['type']} ({behavior})"
        ax.text(x, y - 5, label, color=color, fontsize=10, 
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    # Draw pedestrian bounding boxes
    for pedestrian in annotation.get('pedestrians', []):
        bbox = pedestrian['bbox']
        x, y, w, h = bbox
        
        rect = patches.Rectangle((x, y), w, h, linewidth=2, 
                                 edgecolor='purple', facecolor='none')
        ax.add_patch(rect)
        
        label = f"Pedestrian ({pedestrian.get('action', 'unknown')})"
        ax.text(x, y - 5, label, color='purple', fontsize=10,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    # Add risk level
    risk_level = annotation.get('risk_level', 'unknown')
    ax.text(10, 30, f"Risk Level: {risk_level.upper()}", 
           fontsize=14, color='white',
           bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
    
    ax.axis('off')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def compute_time_to_accident(crash_frame: int, current_frame: int, fps: int) -> float:
    """
    Compute time to accident (TTA) in seconds.
    
    Args:
        crash_frame (int): Frame number where crash occurs
        current_frame (int): Current frame number
        fps (int): Frames per second
        
    Returns:
        float: Time to accident in seconds (negative if past crash)
    """
    return (crash_frame - current_frame) / fps


# Example usage
if __name__ == "__main__":
    # Initialize dataset
    dataset = TCASDataset('/path/to/TCAS-dataset', split='train')
    
    print(f"Dataset size: {len(dataset)} videos")
    
    # Load first video
    sample = dataset[0]
    print(f"\nLoaded video: {sample['video_id']}")
    print(f"Number of frames: {len(sample['frames'])}")
    
    # Get annotation info
    anno = sample['annotation']
    print(f"Category: {anno['category']}")
    if anno['category'] == 'crash':
        print(f"Crash type: {anno.get('crash_type')}")
        print(f"Crash frame: {anno.get('crash_frame')}")
    
    # Print dataset statistics
    stats = dataset.get_statistics()
    print("\nDataset Statistics:")
    print(f"Total videos: {stats['total_videos']}")
    print(f"Total frames: {stats['total_frames']}")
