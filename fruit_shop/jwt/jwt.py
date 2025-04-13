from jose import jwt


class JWTDecoder:
    def get_unverified_payload(self, token: str):
        try:
            payload = jwt.get_unverified_claims(token)
            return payload
        except:
            return "Unable to get payload"