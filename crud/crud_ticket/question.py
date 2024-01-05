from crud.base import CRUDBase
from models import Question
from schemas.ticket.question import QuestionCreate, QuestionUpdate


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    pass


question = CRUDQuestion(Question)
