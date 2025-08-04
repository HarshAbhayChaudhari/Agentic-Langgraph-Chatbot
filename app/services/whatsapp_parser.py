import re
from typing import List, Dict
from datetime import datetime
import os

class WhatsAppParser:
    def __init__(self):
        # Regex pattern for WhatsApp chat export format
        # Format: [DD/MM/YYYY, HH:MM:SS] Sender: Message
        self.message_pattern = r'\[(\d{1,2}/\d{1,2}/\d{4}),\s*(\d{1,2}:\d{2}:\d{2})\]\s*(.+?):\s*(.+)'
        
    def parse_file(self, file_path: str) -> List[Dict]:
        """
        Parse WhatsApp chat export file and extract messages
        """
        messages = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Find all messages using regex
            matches = re.findall(self.message_pattern, content, re.MULTILINE)
            
            for match in matches:
                date_str, time_str, sender, message = match
                
                # Parse date and time
                try:
                    datetime_obj = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")
                except ValueError:
                    continue
                
                # Clean message text
                cleaned_message = self._clean_message(message)
                
                if cleaned_message.strip():
                    messages.append({
                        'date': datetime_obj,
                        'sender': sender.strip(),
                        'message': cleaned_message,
                        'timestamp': datetime_obj.isoformat()
                    })
                    
        except Exception as e:
            print(f"Error parsing file: {str(e)}")
            return []
            
        return messages
    
    def _clean_message(self, message: str) -> str:
        """
        Clean and preprocess message text
        """
        # Remove common WhatsApp artifacts
        cleaned = message.strip()
        
        # Remove media messages
        if any(media_indicator in cleaned.lower() for media_indicator in [
            '<media omitted>', 'image omitted', 'video omitted', 
            'audio omitted', 'document omitted', 'location omitted'
        ]):
            return ""
        
        # Remove URLs (optional - you might want to keep them)
        # cleaned = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', cleaned)
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        return cleaned.strip()
    
    def create_chunks(self, messages: List[Dict], chunk_size: int = 512) -> List[str]:
        """
        Create text chunks from messages for embedding
        """
        chunks = []
        current_chunk = ""
        
        for message in messages:
            message_text = f"[{message['sender']}]: {message['message']}"
            
            # If adding this message would exceed chunk size, save current chunk
            if len(current_chunk + " " + message_text) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = message_text
            else:
                if current_chunk:
                    current_chunk += " " + message_text
                else:
                    current_chunk = message_text
        
        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def filter_messages_by_sender(self, messages: List[Dict], sender: str) -> List[Dict]:
        """
        Filter messages by sender (useful for "YOU" chat)
        """
        return [msg for msg in messages if msg['sender'].lower() == sender.lower()]
    
    def get_message_statistics(self, messages: List[Dict]) -> Dict:
        """
        Get statistics about the parsed messages
        """
        if not messages:
            return {}
        
        senders = set(msg['sender'] for msg in messages)
        total_messages = len(messages)
        date_range = {
            'start': min(msg['date'] for msg in messages),
            'end': max(msg['date'] for msg in messages)
        }
        
        return {
            'total_messages': total_messages,
            'unique_senders': len(senders),
            'senders': list(senders),
            'date_range': date_range
        } 