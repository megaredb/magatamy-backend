from crud.base import CRUDBase
from models import Form
from schemas.ticket.form import FormCreate, FormUpdate


class CRUDForm(CRUDBase[Form, FormCreate, FormUpdate]):
    pass


form = CRUDForm(Form)
