"""Several fixes

Revision ID: 50bf7ee405ec
Revises: 7b6e34392f03
Create Date: 2024-07-27 13:21:23.876033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50bf7ee405ec'
down_revision: Union[str, None] = '7b6e34392f03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'custom_command',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('product', 'connected_form_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'connected_form_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('product', 'custom_command',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
