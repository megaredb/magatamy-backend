from backend.crud.base import CRUDBase
from backend.models import Question
from backend.schemas.ticket.question import QuestionCreate, QuestionUpdate


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    pass


question = CRUDQuestion(Question)
