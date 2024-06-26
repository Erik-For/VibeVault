"""empty message

Revision ID: 6ed313dd6ddd
Revises: a281469da472
Create Date: 2024-01-10 14:37:04.927331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ed313dd6ddd'
down_revision = 'a281469da472'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artists', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verified', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artists', schema=None) as batch_op:
        batch_op.drop_column('verified')

    # ### end Alembic commands ###
