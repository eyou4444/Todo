"""empty message

Revision ID: e5ef70cc7b5e
Revises: 5341c9f1e287
Create Date: 2017-10-07 16:53:08.371106

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e5ef70cc7b5e'
down_revision = '5341c9f1e287'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'asb')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('asb', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    # ### end Alembic commands ###