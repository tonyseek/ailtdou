"""Save token expires time.

Revision ID: 2b4a4f9f720e
Revises: 23835573fccb
Create Date: 2015-02-15 06:16:03.675036

"""

revision = '2b4a4f9f720e'
down_revision = '23835573fccb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'user',
        sa.Column('expires_in', sa.Integer(), default=3920, nullable=True)
    )


def downgrade():
    op.drop_column('user', 'expires_in')
