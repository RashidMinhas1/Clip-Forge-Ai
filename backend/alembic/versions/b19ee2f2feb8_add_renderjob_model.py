"""add_renderjob_model

Revision ID: b19ee2f2feb8
Revises: e919265a4250
Create Date: 2026-08-17 11:59:39.639391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b19ee2f2feb8'
down_revision: Union[str, Sequence[str], None] = 'e919265a4250'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'render_jobs',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('clip_id', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('progress', sa.Float(), nullable=False),
        sa.Column('output_path', sa.String(), nullable=True),
        sa.Column('error_message', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['clip_id'], ['clip_candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_render_jobs_clip_id'), 'render_jobs', ['clip_id'], unique=False)
    op.create_index(op.f('ix_render_jobs_project_id'), 'render_jobs', ['project_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_render_jobs_project_id'), table_name='render_jobs')
    op.drop_index(op.f('ix_render_jobs_clip_id'), table_name='render_jobs')
    op.drop_table('render_jobs')
