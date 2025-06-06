"""pfc

Revision ID: 5aff2e2594ed
Revises: 22b55e7154db
Create Date: 2025-04-30 09:40:08.611346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5aff2e2594ed'
down_revision: Union[str, None] = '22b55e7154db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Dishes', sa.Column('proteins', sa.Integer(), nullable=True))
    op.add_column('Dishes', sa.Column('fats', sa.Integer(), nullable=True))
    op.add_column('Dishes', sa.Column('carbohydrates', sa.Integer(), nullable=True))
    op.add_column('Users', sa.Column('proteins', sa.Integer(), nullable=True))
    op.add_column('Users', sa.Column('fats', sa.Integer(), nullable=True))
    op.add_column('Users', sa.Column('carbohydrates', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'carbohydrates')
    op.drop_column('Users', 'fats')
    op.drop_column('Users', 'proteins')
    op.drop_column('Dishes', 'carbohydrates')
    op.drop_column('Dishes', 'fats')
    op.drop_column('Dishes', 'proteins')
    # ### end Alembic commands ###
