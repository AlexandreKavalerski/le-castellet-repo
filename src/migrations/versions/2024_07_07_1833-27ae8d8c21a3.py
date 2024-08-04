"""create new model Mentorship

Revision ID: 27ae8d8c21a3
Revises: 3b0d1dab7741
Create Date: 2024-07-07 18:33:30.115713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '27ae8d8c21a3'
down_revision: Union[str, None] = '3b0d1dab7741'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('mentorship',
        sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('transcription', sa.Text(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('main_topics', sa.Text(), nullable=True),
        sa.Column('interest_courses', sa.Text(), nullable=True),
        sa.Column('main_questions_and_concerns', sa.Text(), nullable=True),
        sa.Column('insights', sa.Text(), nullable=True),
        sa.Column('recording_location', sa.String(length=200), nullable=True),
        sa.Column('uuid', mysql.CHAR(length=32), nullable=False),
        sa.Column('created_at', mysql.DATETIME(), nullable=False),
        sa.Column('updated_at', mysql.DATETIME(), nullable=True),
        sa.Column('deleted_at', mysql.DATETIME(), nullable=True),
        sa.Column('mentorship_date', mysql.DATETIME(), nullable=True),
        sa.Column('is_deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
        sa.Column('mentor_id', mysql.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('student_id', mysql.INTEGER(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['mentor_id'], ['user.id']),
        sa.ForeignKeyConstraint(['student_id'], ['user.id']),
    )
    op.create_index('uuid', 'mentorship', ['uuid'], unique=True)
    op.create_index('id', 'mentorship', ['id'], unique=True)
    op.create_unique_constraint(None, 'mentorship', ['mentor_id', 'student_id', 'mentorship_date'])


def downgrade() -> None:
    op.drop_table('mentorship')
