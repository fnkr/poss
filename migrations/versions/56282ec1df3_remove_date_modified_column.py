"""remove date_modified column from view, user_agent and referer tables

Revision ID: 56282ec1df3
Revises: 49d44a0167b
Create Date: 2015-02-27 12:23:59.627787

"""

# revision identifiers, used by Alembic.
revision = '56282ec1df3'
down_revision = '49d44a0167b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.drop_column('referrer', 'date_modified')
    op.drop_column('user_agent', 'date_modified')
    op.drop_column('view', 'date_modified')


def downgrade():
    op.add_column('view', sa.Column('date_modified', mysql.DATETIME(), nullable=False))
    op.add_column('user_agent', sa.Column('date_modified', mysql.DATETIME(), nullable=False))
    op.add_column('referrer', sa.Column('date_modified', mysql.DATETIME(), nullable=False))
