"""adding columns to post table

Revision ID: d1663f75b44f
Revises: 92c58ed23349
Create Date: 2022-12-29 18:30:58.804746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1663f75b44f'
down_revision = '92c58ed23349'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
