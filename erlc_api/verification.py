import hmac
import hashlib
import base64


class SVWebhookVerification:
    def __init__(self, secret: str):
        self.secret = secret.encode()

    def verify(self, body: bytes, signature_header: str):
        expected = hmac.new(self.secret, body, hashlib.sha256).digest()
        received = base64.b64decode(signature_header)

        return hmac.compare_digest(expected, received)
