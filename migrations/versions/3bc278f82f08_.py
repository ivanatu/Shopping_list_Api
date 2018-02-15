"""empty message

Revision ID: 3bc278f82f08
Revises: cbafd9ef9586
Create Date: 2017-12-11 12:50:46.243392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bc278f82f08'
down_revision = 'cbafd9ef9586'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=80), nullable=True))
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_unique_constraint(None, 'users', ['email'])
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='unique')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
