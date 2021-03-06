"""empty message

Revision ID: 07a7150aad2b
Revises: 
Create Date: 2018-02-15 12:03:08.623558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07a7150aad2b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=True),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=True),
    sa.Column('password', sa.String(length=500), nullable=True),
    sa.Column('token', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('password')
    )
    op.create_table('shopping_lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('list', sa.String(length=80), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('list')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('List_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['List_id'], ['shopping_lists.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    op.drop_table('shopping_lists')
    op.drop_table('users')
    # ### end Alembic commands ###
