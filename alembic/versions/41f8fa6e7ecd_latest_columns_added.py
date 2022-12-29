"""latest columns added

Revision ID: 41f8fa6e7ecd
Revises: 4971a7e63e09
Create Date: 2022-12-29 18:49:57.583813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41f8fa6e7ecd'
down_revision = '4971a7e63e09'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone='TRUE'), nullable=False,
                  server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
