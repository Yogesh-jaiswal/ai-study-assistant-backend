"""added vector data type in embeddings

Revision ID: 3d063b963dcd
Revises: 7091a6c15ec7
Create Date: 2026-06-25 14:34:25.017105

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3d063b963dcd'
down_revision = '7091a6c15ec7'
branch_labels = None
depends_on = None

def upgrade():
    dialect_name = op.get_bind().dialect.name

    if dialect_name == 'postgresql':
        op.execute(
            "ALTER TABLE chunk_embeddings ALTER COLUMN vector TYPE vector(384) "
            "USING vector::text::vector(384);"
        )
        op.create_index(
            'hnsw_chunk_vector_idx',
            'chunk_embeddings',
            ['vector'],
            postgresql_using='hnsw',
            postgresql_ops={
                'vector': 'vector_cosine_ops'
            }
        )
    else:
        # 2. On SQLite, keep it as standard text storage
        with op.batch_alter_table('chunk_embeddings', schema=None) as batch_op:
            batch_op.alter_column('vector',
                   existing_type=postgresql.JSON(astext_type=sa.Text()),
                   type_=sa.Text(),
                   existing_nullable=False)


def downgrade():
    dialect_name = op.get_bind().dialect.name

    if dialect_name == 'postgresql':
        op.execute(
            "ALTER TABLE chunk_embeddings ALTER COLUMN vector TYPE jsonb "
            "USING vector::text::jsonb;"
        )
        op.drop_index(
            'hnsw_chunk_vector_idx',
            table_name='chunk_embeddings',
            postgresql_using='hnsw'
        )
    else:
        with op.batch_alter_table('chunk_embeddings', schema=None) as batch_op:
            batch_op.alter_column('vector',
                   existing_type=sa.Text(),
                   type_=postgresql.JSON(astext_type=sa.Text()),
                   existing_nullable=False)