from Contents.base_content import BaseContent
from db.Models.csrf_token_model import CsrfToken


class CSRFTokenContent(BaseContent):
    data: CsrfToken
