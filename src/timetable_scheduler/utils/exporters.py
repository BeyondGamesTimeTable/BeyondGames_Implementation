"""Schedule export utilities."""

import json
import csv
from typing import Dict, Any, Optional
from pathlib import Path
from ..models import Schedule


class ScheduleExporter:
    """Utility class for exporting schedules to different formats."""
    
    def __init__(self):
        """Initialize the schedule exporter."""
        self.supported_formats = ['json', 'csv', 'txt']
    
    def export_schedule(self, schedule: Schedule, output_path: str, 
                       format_type: str = 'json') -> bool:
        """
        Export a schedule to the specified format.
        
        Args:
            schedule: Schedule object to export
            output_path: Path to save the exported file
            format_type: Export format ('json', 'csv', 'txt')
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            if format_type.lower() == 'json':
                return self._export_json(schedule, output_path)
            elif format_type.lower() == 'csv':
                return self._export_csv(schedule, output_path)
            elif format_type.lower() == 'txt':
                return self._export_txt(schedule, output_path)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def _export_json(self, schedule: Schedule, output_path: str) -> bool:
        """Export schedule to JSON format."""
        schedule_data = schedule.to_dict()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(schedule_data, f, indent=2, ensure_ascii=False)
        
        return True
    
    def _export_csv(self, schedule: Schedule, output_path: str) -> bool:
        """Export schedule to CSV format."""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            header = ['Assignment ID', 'Course ID', 'Professor ID', 'Room ID', 'Time Slot ID', 'Session Number']
            writer.writerow(header)
            
            # Write assignments
            for assignment in schedule.assignments:
                row = [
                    assignment.id,
                    assignment.course_id,
                    assignment.professor_id,
                    assignment.room_id,
                    assignment.time_slot_id,
                    assignment.session_number
                ]
                writer.writerow(row)
        
        return True
    
    def _export_txt(self, schedule: Schedule, output_path: str) -> bool:
        """Export schedule to text format."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Timetable Schedule: {schedule.name}\n")
            f.write(f"Generated on: {schedule.created_at}\n")
            f.write(f"Algorithm: {schedule.algorithm_used}\n")
            f.write(f"Quality Score: {schedule.quality_score}\n")
            f.write("=" * 50 + "\n\n")
            
            for assignment in schedule.assignments:
                f.write(f"Course: {assignment.course_id}\n")
                f.write(f"Professor: {assignment.professor_id}\n")
                f.write(f"Room: {assignment.room_id}\n")
                f.write(f"Time Slot: {assignment.time_slot_id}\n")
                f.write(f"Session: {assignment.session_number}\n")
                f.write("-" * 30 + "\n")
        
        return True