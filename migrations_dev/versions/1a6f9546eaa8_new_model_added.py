"""new Model added

Revision ID: 1a6f9546eaa8
Revises: edf15ba5b723
Create Date: 2020-07-29 11:38:09.140315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a6f9546eaa8'
down_revision = 'edf15ba5b723'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('challenge3',
    sa.Column('challenge_id', sa.Integer(), nullable=False),
    sa.Column('challenge', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('challenge_id')
    )
    op.drop_index('ix_users_username', table_name='users')
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.drop_table('challenge3')
    # ### end Alembic commands ###
