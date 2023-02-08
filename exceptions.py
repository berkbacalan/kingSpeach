
class NoAudioDevice(Exception):
    """Exception raised for errors when no audio device found.

    Attributes:
        message: error description
    """
    def __init__(self, msg='Audio I/O device not found', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class RecordDurationTooLong(Exception):
    """Exception raised for errors when record duration greather than 2700 seconds.

    Attributes:
        message: error description
    """
    def __init__(self, msg='The recording duration cannot exceed 2700 seconds.', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)