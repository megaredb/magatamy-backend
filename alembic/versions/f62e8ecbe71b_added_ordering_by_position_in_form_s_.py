"""Added ordering by position in form's questions.

Revision ID: f62e8ecbe71b
Revises: aa360767967f
Create Date: 2024-01-07 20:45:04.742230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f62e8ecbe71b'
down_revision: Union[str, None] = 'aa360767967f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
