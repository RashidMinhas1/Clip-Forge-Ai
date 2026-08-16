"""create_transcription_tables

Revision ID: a3f92c1e8b47
Revises: 54e4a11d6d6a
Create Date: 2026-08-16 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3f92c1e8b47'
down_revision: Union[str, Sequence[str], None] = '54e4a11d6d6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create transcripts table
    op.create_table(
        'transcripts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('source_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('language', sa.String(), nullable=True),
        sa.Column('duration', sa.Float(), nullable=True),
        sa.Column('model_used', sa.String(), nullable=True),
        sa.Column('error_message', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_transcripts_source_id'), 'transcripts', ['source_id'], unique=False)

    # Create transcript_segments table
    op.create_table(
        'transcript_segments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('transcript_id', sa.UUID(), nullable=False),
        sa.Column('segment_index', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.Float(), nullable=False),
        sa.Column('end_time', sa.Float(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['transcript_id'], ['transcripts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_transcript_segments_transcript_id'), 'transcript_segments', ['transcript_id'], unique=False)

    # Create transcript_words table
    op.create_table(
        'transcript_words',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('segment_id', sa.UUID(), nullable=False),
        sa.Column('word_index', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.Float(), nullable=False),
        sa.Column('end_time', sa.Float(), nullable=False),
        sa.Column('word', sa.String(), nullable=False),
        sa.Column('probability', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['segment_id'], ['transcript_segments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_transcript_words_segment_id'), 'transcript_words', ['segment_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_transcript_words_segment_id'), table_name='transcript_words')
    op.drop_table('transcript_words')
    op.drop_index(op.f('ix_transcript_segments_transcript_id'), table_name='transcript_segments')
    op.drop_table('transcript_segments')
    op.drop_index(op.f('ix_transcripts_source_id'), table_name='transcripts')
    op.drop_table('transcripts')
