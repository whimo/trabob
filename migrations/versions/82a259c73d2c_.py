"""empty message

Revision ID: 82a259c73d2c
Revises: 5b4c4a47f3bb
Create Date: 2017-07-06 14:37:27.273537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82a259c73d2c'
down_revision = '5b4c4a47f3bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('is_roman', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('account', 'is_roman')
    # ### end Alembic commands ###
