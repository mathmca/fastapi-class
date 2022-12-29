"""add foreing-key to post table

Revision ID: 4971a7e63e09
Revises: 4c4a959392fa
Create Date: 2022-12-29 18:44:44.866619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4971a7e63e09'
down_revision = '4c4a959392fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('user_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
