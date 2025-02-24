"""empty message

Revision ID: 376d9b709a13
Revises: 
Create Date: 2024-10-29 02:14:28.691898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '376d9b709a13'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('price', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'product', ['id'])
    op.create_unique_constraint(None, 'signup', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'signup', type_='unique')
    op.drop_constraint(None, 'product', type_='unique')
    op.drop_column('product', 'price')
    # ### end Alembic commands ###
