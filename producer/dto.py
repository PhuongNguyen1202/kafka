from typing import Optional
from pydantic import BaseModel


# Model để xác định kiểu dữ liệu của request body
class MessageDto(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None
    partition: Optional[int] = None
