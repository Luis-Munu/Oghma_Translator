import json
import pandas as pd
from typing import Dict, Any
from config import Config

def load_progress(config: Config) -> Dict[str, Any]:
    if config.progress_file.exists():
        try:
            with config.progress_file.open('r', encoding='utf-8') as f:
                progress = json.load(f)
                progress.setdefault('completed_sheets', [])
                progress.setdefault('current_indices', {})
                progress.setdefault('successful_translations', 0)
                progress.setdefault('next_save_at', progress['successful_translations'] + config.save_interval)
                # Ensure 'current_indices' values are integers
                for sheet, cols in progress.get('current_indices', {}).items():
                    for col, row in cols.items():
                        progress['current_indices'][sheet][col] = int(row)
                return progress
        except (json.JSONDecodeError, IOError) as e:
            print(f"Failed to load progress file. Starting fresh. Error: {e}")
    return {
        'completed_sheets': [],
        'current_indices': {},
        'successful_translations': 0,
        'next_save_at': config.save_interval,
        'timestamp': pd.Timestamp.now().isoformat()
    }

def save_progress(progress_data: Dict[str, Any], config: Config, workbook):
    try:
        with config.progress_file.open('w', encoding='utf-8') as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=4)
        print(f"Progress saved at {progress_data['successful_translations']} translations.")
        workbook.save(config.output_file)
        print(f"File saved at {progress_data['successful_translations']} translations.")
    except IOError as e:
        print(f"Failed to save progress: {e}")