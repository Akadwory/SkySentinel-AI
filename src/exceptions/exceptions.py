class KafkaConnectionError(Exception):
    """Raised when there is an issue connecting to Kafka."""
    pass

class DataProcessingError(Exception):
    """Raised for errors during data processing."""
    pass
