from schemas.base import BaseComplaint
from datetime import datetime
from models import State


class ComplaintOut(BaseComplaint):
    id: int
    created_at: datetime
    state: State
