# src/utils/file_handler.py
import json
import os
from datetime import datetime

class ConversationHandler:
    def __init__(self, base_path='data/conversation_history'):
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)
    
    def get_filename(self):
        return f"history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def save_conversation(self, history, filename=None):
        if filename is None:
            filename = self.get_filename()
        filepath = os.path.join(self.base_path, filename)
        with open(filepath, 'w') as f:
            json.dump(history, f)
        return filename
    
    def load_conversation(self, filename):
        filepath = os.path.join(self.base_path, filename)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def get_all_histories(self):
        histories = []
        for filename in os.listdir(self.base_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.base_path, filename)
                with open(filepath, 'r') as f:
                    history = json.load(f)
                    histories.append({
                        'filename': filename,
                        'timestamp': filename.split('_')[1].split('.')[0],
                        'messages': history
                    })
        return sorted(histories, key=lambda x: x['timestamp'], reverse=True)