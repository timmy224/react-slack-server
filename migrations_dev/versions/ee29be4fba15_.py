"""empty message

Revision ID: ee29be4fba15
Revises: 52a4e9308e5a
Create Date: 2020-09-08 15:54:39.997946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee29be4fba15'
down_revision = '52a4e9308e5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actions',
    sa.Column('action_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('action_id')
    )
    op.create_table('resources',
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('resource_id')
    )
    op.add_column('permissions', sa.Column('action_id', sa.Integer(), nullable=True))
    op.add_column('permissions', sa.Column('resource_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'permissions', 'actions', ['action_id'], ['action_id'])
    op.create_foreign_key(None, 'permissions', 'resources', ['resource_id'], ['resource_id'])
    op.drop_column('permissions', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('permissions', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'permissions', type_='foreignkey')
    op.drop_constraint(None, 'permissions', type_='foreignkey')
    op.drop_column('permissions', 'resource_id')
    op.drop_column('permissions', 'action_id')
    op.drop_table('resources')
    op.drop_table('actions')
    # ### end Alembic commands ###