import re
from typing import List, Dict
from datetime import datetime

class WhatsAppParser:
    def __init__(self):
        """
        Initialize WhatsApp parser
        """
        # Regex pattern for WhatsApp message format
        self.message_pattern = r'\[(\d{1,2}/\d{1,2}/\d{4}),\s*(\d{1,2}:\d{2}:\d{2})\]\s*(.+?):\s*(.+)'
    
    def parse_file(self, file_path: str) -> List[Dict]:
        """
        Parse WhatsApp chat export file
        
        Args:
            file_path: Path to the chat export file
            
        Returns:
            List of parsed messages
        """
        messages = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Split content into lines
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Parse message using regex
                match = re.match(self.message_pattern, line)
                if match:
                    date_str, time_str, sender, message = match.groups()
                    
                    # Parse date and time
                    try:
                        date_time = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")
                    except ValueError:
                        # Try alternative format
                        try:
                            date_time = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M:%S")
                        except ValueError:
                            date_time = datetime.now()
                    
                    messages.append({
                        'date': date_time,
                        'sender': sender.strip(),
                        'message': message.strip(),
                        'raw_line': line
                    })
                else:
                    # Handle multi-line messages or system messages
                    if messages:
                        # Append to the last message if it's a continuation
                        messages[-1]['message'] += '\n' + line
                    else:
                        # System message or unrecognized format
                        messages.append({
                            'date': datetime.now(),
                            'sender': 'System',
                            'message': line,
                            'raw_line': line
                        })
            
            print(f"Parsed {len(messages)} messages from file")
            return messages
            
        except Exception as e:
            print(f"Error parsing file: {str(e)}")
            raise
    
    def create_chunks(self, messages: List[Dict], chunk_size: int = 512) -> List[str]:
        """
        Create text chunks from messages for embedding
        
        Args:
            messages: List of parsed messages
            chunk_size: Maximum size of each chunk
            
        Returns:
            List of text chunks
        """
        chunks = []
        current_chunk = ""
        
        for message in messages:
            # Format message
            formatted_message = f"[{message['date'].strftime('%d/%m/%Y %H:%M:%S')}] {message['sender']}: {message['message']}\n"
            
            # Check if adding this message would exceed chunk size
            if len(current_chunk) + len(formatted_message) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = formatted_message
            else:
                current_chunk += formatted_message
        
        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        print(f"Created {len(chunks)} chunks from {len(messages)} messages")
        return chunks
    
    def filter_messages_by_date(self, messages: List[Dict], start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        """
        Filter messages by date range
        
        Args:
            messages: List of parsed messages
            start_date: Start date for filtering
            end_date: End date for filtering
            
        Returns:
            Filtered list of messages
        """
        filtered_messages = []
        
        for message in messages:
            message_date = message['date']
            
            if start_date and message_date < start_date:
                continue
            if end_date and message_date > end_date:
                continue
                
            filtered_messages.append(message)
        
        return filtered_messages
    
    def filter_messages_by_sender(self, messages: List[Dict], sender: str) -> List[Dict]:
        """
        Filter messages by sender
        
        Args:
            messages: List of parsed messages
            sender: Sender name to filter by
            
        Returns:
            Filtered list of messages
        """
        return [msg for msg in messages if msg['sender'].lower() == sender.lower()] 