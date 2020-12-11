"""object encrypted

Revision ID: e377b575cbde
Revises: 56282ec1df3
Create Date: 2020-12-11 11:39:22.057854

"""

# revision identifiers, used by Alembic.
revision = 'e377b575cbde'
down_revision = '56282ec1df3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('object', sa.Column('encrypted', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('object', 'encrypted')
