"""add framing_mode to clip_candidates

Revision ID: d4e5f6g7h8i9
Revises: c1d2e3f4g5h6
Create Date: 2026-08-17 11:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd4e5f6g7h8i9'
down_revision = 'c1d2e3f4g5h6'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # add framing_mode column to clip_candidates with a default value of ORIGINAL
    op.add_column('clip_candidates', sa.Column('framing_mode', sa.String(), server_default='ORIGINAL', nullable=False))

def downgrade() -> None:
    op.drop_column('clip_candidates', 'framing_mode')
