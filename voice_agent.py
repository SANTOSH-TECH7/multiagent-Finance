class VoiceAgent:
    def __init__(self):
        self.name = "Voice Processing Agent"

    def text_to_speech_info(self, text):
        word_count = len(text.split())
        estimated_duration = word_count / 150 * 60
        return {
            'text': text,
            'word_count': word_count,
            'estimated_duration_seconds': round(estimated_duration, 1),
            'status': 'ready_for_tts'
        }