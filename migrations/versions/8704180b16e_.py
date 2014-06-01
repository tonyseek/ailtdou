"""Initial database.

Revision ID: 8704180b16e
Revises: None
Create Date: 2014-06-02 00:53:17.264867

"""

revision = '8704180b16e'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('access_token', sa.Unicode(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'activity',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('subject', sa.Unicode(length=60), nullable=True),
        sa.Column('text', sa.UnicodeText(), nullable=True),
        sa.Column('time', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], [u'user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('activity')
    op.drop_table('user')
