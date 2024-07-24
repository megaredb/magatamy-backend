from backend.crud.base import CRUDBase
from backend.models import Form
from backend.schemas.ticket.form import FormCreate, FormUpdate


class CRUDForm(CRUDBase[Form, FormCreate, FormUpdate]):
    pass


form = CRUDForm(Form)
