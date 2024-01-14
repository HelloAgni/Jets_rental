"""User Jet Rental

Revision ID: cdbbdd6b379b
Revises: 
Create Date: 2024-01-14 15:37:11.057192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdbbdd6b379b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('jet_type', sa.String(length=25), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('speed', sa.Integer(), nullable=False),
    sa.Column('flight_range', sa.Integer(), nullable=False),
    sa.Column('passenger_capacity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    # sa.Column('id', sa.Integer(), nullable=False),
    sa.CheckConstraint('length(name) > 3', name=op.f('ck_jet_')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_jet')),
    sa.UniqueConstraint('name', name=op.f('uq_jet_name'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    # sa.Column('id', sa.Integer(), nullable=False),
    sa.CheckConstraint('length(first_name) > 3 and length(last_name) > 3', name='length_min4'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)

    op.create_table('rental',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('jet_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    # sa.Column('id', sa.Integer(), nullable=False),
    sa.CheckConstraint('start_date < end_date', name=op.f('ck_rental_')),
    sa.ForeignKeyConstraint(['jet_id'], ['jet.id'], name=op.f('fk_rental_jet_id_jet')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_rental_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_rental'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rental')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('jet')
    # ### end Alembic commands ###
