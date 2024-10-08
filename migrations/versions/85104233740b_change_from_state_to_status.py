"""change from state to status

Revision ID: 85104233740b
Revises: 814040d0f16d
Create Date: 2024-07-20 03:12:27.511084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '85104233740b'
down_revision: Union[str, None] = '814040d0f16d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('complaints', sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='state'), server_default='pending', nullable=True))
    op.drop_column('complaints', 'state')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('complaints', sa.Column('state', postgresql.ENUM('pending', 'approved', 'rejected', name='state'), server_default=sa.text("'pending'::state"), autoincrement=False, nullable=True))
    op.drop_column('complaints', 'status')
    # ### end Alembic commands ###
