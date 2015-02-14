"""Save token expires time.

Revision ID: 691639bdcf1
Revises: 2b4a4f9f720e
Create Date: 2015-02-15 06:28:57.079032

"""

revision = '691639bdcf1'
down_revision = '2b4a4f9f720e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'user',
        sa.Column('expires_at', sa.Integer(), default=0)
    )


def downgrade():
    op.drop_column('user', 'expires_at')
