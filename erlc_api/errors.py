class SVError(Exception):
    """Base error for SVAPIHELPER:LC"""


class AuthenticationError(SVError):
    """Invalid API key"""


class NotFoundError(SVError):
    """Requested ERLC resource does not exist"""


class RateLimitError(SVError):
    """ERLC API limit reached"""


class UnknownAPIError(SVError):
    """Unexpected ERLC API response"""
