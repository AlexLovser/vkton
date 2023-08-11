class TimeoutResponseError(TimeoutError):
    pass

class NoContentError(ValueError):
    pass

class CancelError(ValueError):
    pass

class LessPermissionsError(PermissionError):
    pass

class UnknownCommandError(ValueError):
    pass


class BadImageSizeError(ValueError):
    pass

class InvalidImageError(ValueError):
    pass

class PhotoUploadHasFailedError(ValueError):
    pass


