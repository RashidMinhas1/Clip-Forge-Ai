"""ms009 clipping

Revision ID: c1d2e3f4g5h6
Revises: a3f92c1e8b47
Create Date: 2026-08-16 11:34:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c1d2e3f4g5h6'
down_revision: Union[str, None] = 'a3f92c1e8b47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('clip_discovery_runs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('source_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('error_message', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clip_discovery_runs_project_id'), 'clip_discovery_runs', ['project_id'], unique=False)
    op.create_index(op.f('ix_clip_discovery_runs_source_id'), 'clip_discovery_runs', ['source_id'], unique=False)

    op.create_table('clip_candidates',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('run_id', sa.UUID(), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('hook', sa.String(), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('start_time', sa.Float(), nullable=False),
        sa.Column('end_time', sa.Float(), nullable=False),
        sa.Column('duration', sa.Float(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('transcript_excerpt', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['run_id'], ['clip_discovery_runs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clip_candidates_project_id'), 'clip_candidates', ['project_id'], unique=False)
    op.create_index(op.f('ix_clip_candidates_run_id'), 'clip_candidates', ['run_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_clip_candidates_run_id'), table_name='clip_candidates')
    op.drop_index(op.f('ix_clip_candidates_project_id'), table_name='clip_candidates')
    op.drop_table('clip_candidates')
    op.drop_index(op.f('ix_clip_discovery_runs_source_id'), table_name='clip_discovery_runs')
    op.drop_index(op.f('ix_clip_discovery_runs_project_id'), table_name='clip_discovery_runs')
    op.drop_table('clip_discovery_runs')
