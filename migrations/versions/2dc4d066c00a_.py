"""empty message

Revision ID: 2dc4d066c00a
Revises: 
Create Date: 2018-10-10 12:48:29.851796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dc4d066c00a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('casedata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('well', sa.String(length=64), nullable=True),
    sa.Column('readdate', sa.String(length=15), nullable=True),
    sa.Column('oilrate', sa.Float(), nullable=True),
    sa.Column('waterrate', sa.Float(), nullable=True),
    sa.Column('gasrate', sa.Float(), nullable=True),
    sa.Column('user', sa.String(length=64), nullable=True),
    sa.Column('datasetname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_casedata_user'), 'casedata', ['user'], unique=False)
    op.create_index(op.f('ix_casedata_well'), 'casedata', ['well'], unique=False)
    op.create_table('dataset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('well', sa.String(length=64), nullable=True),
    sa.Column('date', sa.String(length=15), nullable=True),
    sa.Column('prod', sa.Float(), nullable=True),
    sa.Column('WATER_PROD', sa.Float(), nullable=True),
    sa.Column('GWG_PROD', sa.Float(), nullable=True),
    sa.Column('CO2_PROD', sa.Float(), nullable=True),
    sa.Column('WATER_INJ', sa.Float(), nullable=True),
    sa.Column('CO2_INJ', sa.Float(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('month', sa.Integer(), nullable=True),
    sa.Column('user', sa.String(length=64), nullable=True),
    sa.Column('datasetname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dataset_datasetname'), 'dataset', ['datasetname'], unique=False)
    op.create_index(op.f('ix_dataset_user'), 'dataset', ['user'], unique=False)
    op.create_index(op.f('ix_dataset_well'), 'dataset', ['well'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_dataset_well'), table_name='dataset')
    op.drop_index(op.f('ix_dataset_user'), table_name='dataset')
    op.drop_index(op.f('ix_dataset_datasetname'), table_name='dataset')
    op.drop_table('dataset')
    op.drop_index(op.f('ix_casedata_well'), table_name='casedata')
    op.drop_index(op.f('ix_casedata_user'), table_name='casedata')
    op.drop_table('casedata')
    # ### end Alembic commands ###
