"""empty message

Revision ID: 3c1179507bb5
Revises: 
Create Date: 2019-02-21 10:04:16.407315

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3c1179507bb5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('client_id', table_name='client')
    op.drop_table('client')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('client_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('client_key', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('client_secret', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('status', mysql.VARCHAR(length=10), nullable=True),
    sa.PrimaryKeyConstraint('client_id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_index('client_id', 'client', ['client_id'], unique=True)
    # ### end Alembic commands ###
