"""Add ClipCaptionConfig model

Revision ID: e919265a4250
Revises: d4e5f6g7h8i9
Create Date: 2026-08-17 11:39:22.485228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e919265a4250'
down_revision: Union[str, Sequence[str], None] = 'd4e5f6g7h8i9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'clip_caption_configs',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('clip_id', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('preset_name', sa.String(), nullable=False),
        sa.Column('font_family', sa.String(), nullable=True),
        sa.Column('font_size', sa.Integer(), nullable=True),
        sa.Column('text_color', sa.String(), nullable=True),
        sa.Column('highlight_color', sa.String(), nullable=True),
        sa.Column('bg_color', sa.String(), nullable=True),
        sa.Column('is_rtl', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['clip_id'], ['clip_candidates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clip_caption_configs_clip_id'), 'clip_caption_configs', ['clip_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_clip_caption_configs_clip_id'), table_name='clip_caption_configs')
    op.drop_table('clip_caption_configs')
