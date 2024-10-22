from main.generative.services.audio_handler import AudioService
from main.generative.services.document_handler import DocumentService
from main.generative.services.quiz_handler import QuizService
from main.generative.services.text_handler import SummaryService, ChatService


class Service:
    def __init__(self, model):
        """Initialize with the model to be used by services."""
        self.model = model

    def get_service(self, service_type):
        """Return the appropriate service based on the service type."""
        if service_type == "summary":
            return SummaryService(self.model)
        elif service_type == "chat":
            return ChatService(self.model)
        elif service_type == "document":
            return DocumentService(self.model)
        elif service_type == "quiz":
            return QuizService(self.model)
        elif service_type == "audio":
            return AudioService("en-AU-WilliamNeural")
        raise ValueError(f"Invalid service type: {service_type}")