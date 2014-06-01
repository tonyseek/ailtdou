"""Save refresh token.

Revision ID: 23835573fccb
Revises: 8704180b16e
Create Date: 2014-06-02 00:56:33.801835

"""

revision = '23835573fccb'
down_revision = '8704180b16e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'user',
        sa.Column('refresh_token', sa.Unicode(), nullable=True)
    )


def downgrade():
    op.drop_column('user', 'refresh_token')
