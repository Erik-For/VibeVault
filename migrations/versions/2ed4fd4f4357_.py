"""empty message

Revision ID: 2ed4fd4f4357
Revises: 9a02b1872ed4
Create Date: 2023-12-08 02:34:45.838429

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2ed4fd4f4357'
down_revision = '9a02b1872ed4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('email_verification_token')
        batch_op.drop_column('email_verified')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email_verified', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('email_verification_token', mysql.VARCHAR(length=32), nullable=True))

    # ### end Alembic commands ###
