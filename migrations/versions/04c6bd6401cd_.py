"""empty message

Revision ID: 04c6bd6401cd
Revises: 
Create Date: 2018-10-31 16:40:59.422374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04c6bd6401cd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Equations',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('Description', sa.String(length=21845), nullable=True),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('MeasurementTypes',
    sa.Column('Id', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('Users',
    sa.Column('IsDeleted', sa.Boolean(), nullable=False),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.Column('ModifiedById', sa.Integer(), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['ModifiedById'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Users_email'), 'Users', ['email'], unique=True)
    op.create_index(op.f('ix_Users_token'), 'Users', ['token'], unique=True)
    op.create_index(op.f('ix_Users_username'), 'Users', ['username'], unique=True)
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
    op.create_table('UploadSets',
    sa.Column('IsDeleted', sa.Boolean(), nullable=False),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('CreatedDate', sa.DateTime(), nullable=False),
    sa.Column('Description', sa.String(length=21845), nullable=True),
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.Column('FileName', sa.String(length=45), nullable=True),
    sa.Column('StoredFileName', sa.String(length=45), nullable=True),
    sa.Column('ModifiedById', sa.Integer(), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['ModifiedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['UserId'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('Wells',
    sa.Column('IsDeleted', sa.Boolean(), nullable=False),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('Latitude', sa.Numeric(precision=11, scale=8), nullable=True),
    sa.Column('Longitude', sa.Numeric(precision=11, scale=8), nullable=True),
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.Column('UploadSetId', sa.Integer(), nullable=True),
    sa.Column('PerforationTopDepth', sa.Float(), nullable=True),
    sa.Column('PerforationBottomDepth', sa.Float(), nullable=True),
    sa.Column('ModifiedById', sa.Integer(), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['ModifiedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['UploadSetId'], ['UploadSets.Id'], ),
    sa.ForeignKeyConstraint(['UserId'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('IDCAnalysis',
    sa.Column('IsDeleted', sa.Boolean(), nullable=False),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('WellId', sa.Integer(), nullable=False),
    sa.Column('Date', sa.DateTime(), nullable=False),
    sa.Column('TotalError', sa.Float(), nullable=True),
    sa.Column('PredictedProduction', sa.Float(), nullable=True),
    sa.Column('ActualProduction', sa.Float(), nullable=True),
    sa.Column('Difference', sa.Float(), nullable=True),
    sa.Column('ModifiedById', sa.Integer(), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['ModifiedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['WellId'], ['Wells.Id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('MeasurementFormats',
    sa.Column('IsDeleted', sa.Boolean(), nullable=False),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('WellId', sa.Integer(), nullable=False),
    sa.Column('MeasurementTypeId', sa.String(length=45), nullable=False),
    sa.Column('Format', sa.String(length=45), nullable=False),
    sa.Column('ModifiedById', sa.Integer(), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['MeasurementTypeId'], ['MeasurementTypes.Id'], ),
    sa.ForeignKeyConstraint(['ModifiedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['WellId'], ['Wells.Id'], ),
    sa.PrimaryKeyConstraint('WellId', 'MeasurementTypeId')
    )
    op.create_table('WellOutputMeasurements',
    sa.Column('IsDeleted', sa.Boolean(), nullable=False),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Date', sa.DateTime(), nullable=False),
    sa.Column('WellId', sa.Integer(), nullable=False),
    sa.Column('MeasurementTypeId', sa.String(length=45), nullable=False),
    sa.Column('Value', sa.Float(), nullable=True),
    sa.Column('ModifiedById', sa.Integer(), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['MeasurementTypeId'], ['MeasurementTypes.Id'], ),
    sa.ForeignKeyConstraint(['ModifiedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['WellId'], ['Wells.Id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('IDCAResults',
    sa.Column('IsDeleted', sa.Boolean(), nullable=False),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('IDCAnalysisId', sa.Integer(), nullable=False),
    sa.Column('StartSegment', sa.Integer(), nullable=False),
    sa.Column('EndSegment', sa.Integer(), nullable=False),
    sa.Column('EquationId', sa.Integer(), nullable=False),
    sa.Column('ParameterA', sa.Float(), nullable=False),
    sa.Column('ParameterB', sa.Float(), nullable=False),
    sa.Column('ModifiedById', sa.Integer(), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedById'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['EquationId'], ['Equations.Id'], ),
    sa.ForeignKeyConstraint(['IDCAnalysisId'], ['IDCAnalysis.Id'], ),
    sa.ForeignKeyConstraint(['ModifiedById'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('IDCAResults')
    op.drop_table('WellOutputMeasurements')
    op.drop_table('MeasurementFormats')
    op.drop_table('IDCAnalysis')
    op.drop_table('Wells')
    op.drop_table('UploadSets')
    op.drop_index(op.f('ix_casedata_well'), table_name='casedata')
    op.drop_index(op.f('ix_casedata_user'), table_name='casedata')
    op.drop_table('casedata')
    op.drop_index(op.f('ix_Users_username'), table_name='Users')
    op.drop_index(op.f('ix_Users_token'), table_name='Users')
    op.drop_index(op.f('ix_Users_email'), table_name='Users')
    op.drop_table('Users')
    op.drop_table('MeasurementTypes')
    op.drop_table('Equations')
    # ### end Alembic commands ###