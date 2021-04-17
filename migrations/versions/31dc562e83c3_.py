"""empty message

Revision ID: 31dc562e83c3
Revises: 
Create Date: 2021-04-17 21:41:41.280489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31dc562e83c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('mascota',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idUser', sa.Integer(), nullable=True),
    sa.Column('nombre', sa.String(length=120), nullable=False),
    sa.Column('edad', sa.Integer(), nullable=False),
    sa.Column('peso', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idUser'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mascota')
    op.drop_table('user')
    # ### end Alembic commands ###
