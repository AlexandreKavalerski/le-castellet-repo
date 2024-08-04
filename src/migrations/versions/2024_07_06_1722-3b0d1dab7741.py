"""add new properties to User

Revision ID: 3b0d1dab7741
Revises: 
Create Date: 2024-07-06 17:22:03.006604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '3b0d1dab7741'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('phone_number', sa.BigInteger(), nullable=True))
    op.add_column('user', sa.Column('user_type', sa.String(length=30), nullable=True))
    op.add_column('user', sa.Column('profile_short_bio', sa.String(length=255), nullable=True))
    op.add_column('user', sa.Column('profile_is_graduated', sa.Boolean(), server_default="0", nullable=True))
    op.add_column('user', sa.Column('profile_age', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'user', ['phone_number'])


def downgrade() -> None:
    op.drop_column('user', 'phone_number')
    op.drop_column('user', 'user_type')
    op.drop_column('user', 'profile_short_bio')
    op.drop_column('user', 'profile_is_graduated')
    op.drop_column('user', 'profile_age')
