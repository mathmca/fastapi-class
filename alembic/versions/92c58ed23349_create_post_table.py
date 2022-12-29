"""create post table

Revision ID: 92c58ed23349
Revises: 
Create Date: 2022-12-29 18:18:20.418623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92c58ed23349'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )
    pass

def downgrade() -> None:
    op.drop_table('posts')
    pass
