"""init

Revision ID: 73184b64cbe3
Revises: 
Create Date: 2020-07-16 20:05:23.333848

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '73184b64cbe3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('_ps_resources',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('resource_table', sa.String(length=500), nullable=True),
    sa.Column('resource_name', sa.String(length=600), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('resource_table')
    )
    op.create_table('_ps_user_groups',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('group', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('group')
    )
    op.create_table('_ps_permissions',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('group', sa.String(length=500), nullable=True),
    sa.Column('resource', sa.String(length=500), nullable=True),
    sa.Column('create', sa.Boolean(), nullable=True),
    sa.Column('read', sa.Boolean(), nullable=True),
    sa.Column('update', sa.Boolean(), nullable=True),
    sa.Column('delete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['group'], ['_ps_user_groups.group'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['resource'], ['_ps_resources.resource_table'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('_ps_users',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('user_name', sa.String(length=500), nullable=True),
    sa.Column('password', sa.String(length=1000), nullable=True),
    sa.Column('group', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['group'], ['_ps_user_groups.group'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_ps_users')
    op.drop_table('_ps_permissions')
    op.drop_table('_ps_user_groups')
    op.drop_table('_ps_resources')
    # ### end Alembic commands ###
