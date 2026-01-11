import re

class TextCleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Normalizes text by removing excessive whitespace and common OCR artifacts.
        """
        if not text:
            return ""
        
        # Replace multiple newlines/tabs with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove non-printable characters (keep basic ASCII + common symbols)
        # simplistic approach: keep alphanumeric and punctuation
        # text = re.sub(r'[^\x20-\x7E]', '', text) 
        
        return text.strip()

    @staticmethod
    def redact_pii(text: str) -> str:
        """
        Redacts emails and phone numbers from the text.
        """
        if not text:
            return ""
            
        # Redact Emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = re.sub(email_pattern, '[EMAIL_REDACTED]', text)
        
        # Redact Phone Numbers (Basic US/Intl format)
        phone_pattern = r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b'
        text = re.sub(phone_pattern, '[PHONE_REDACTED]', text)
        
        return text
