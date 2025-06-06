"""Make first_name and last_name nullable

Revision ID: 4cc0295aaf50
Revises: 35e5e073a39f
Create Date: 2025-05-31 23:51:50.780093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cc0295aaf50'
down_revision: Union[str, None] = '35e5e073a39f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'first_name',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('user', 'last_name',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'last_name',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('user', 'first_name',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###
