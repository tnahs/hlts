"""beta db model

Revision ID: abf3beba6508
Revises:
Create Date: 2018-10-18 00:17:38.069153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abf3beba6508'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
       sa.Column('id', sa.String(length=64), nullable=False),
       sa.Column('name', sa.Text(), nullable=True),
       sa.Column('pinged', sa.DateTime(), nullable=False),
       sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_authors_name'), 'authors', ['name'], unique=False)
    op.create_index(op.f('ix_authors_pinged'), 'authors', ['pinged'], unique=False)
    op.create_table('collections',
       sa.Column('id', sa.Integer(), nullable=False),
       sa.Column('name', sa.Text(), nullable=False),
       sa.Column('color', sa.Text(), nullable=True),
       sa.Column('pinned', sa.Boolean(), nullable=True),
       sa.Column('description', sa.Text(), nullable=True),
       sa.Column('pinged', sa.DateTime(), nullable=False),
       sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_collections_name'), 'collections', ['name'], unique=True)
    op.create_index(op.f('ix_collections_pinged'), 'collections', ['pinged'], unique=False)
    op.create_table('tags',
       sa.Column('id', sa.Integer(), nullable=False),
       sa.Column('name', sa.Text(), nullable=False),
       sa.Column('color', sa.Text(), nullable=True),
       sa.Column('pinned', sa.Boolean(), nullable=True),
       sa.Column('description', sa.Text(), nullable=True),
       sa.Column('pinged', sa.DateTime(), nullable=False),
       sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tags_name'), 'tags', ['name'], unique=True)
    op.create_index(op.f('ix_tags_pinged'), 'tags', ['pinged'], unique=False)
    op.create_table('users',
       sa.Column('id', sa.Integer(), nullable=False),
       sa.Column('username', sa.String(length=32), nullable=False),
       sa.Column('fullname', sa.String(length=32), nullable=False),
       sa.Column('email', sa.String(length=64), nullable=False),
       sa.Column('password', sa.String(length=256), nullable=True),
       sa.Column('is_admin', sa.Boolean(), nullable=True),
       sa.Column('theme_index', sa.Integer(), nullable=True),
       sa.Column('results_per_page', sa.Integer(), nullable=True),
       sa.Column('recent_days', sa.Integer(), nullable=True),
       sa.Column('api_key', sa.String(length=64), nullable=True),
       sa.PrimaryKeyConstraint('id'),
       sa.UniqueConstraint('email'),
       sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_api_key'), 'users', ['api_key'], unique=True)
    op.create_table('sources',
       sa.Column('id', sa.String(length=64), nullable=False),
       sa.Column('name', sa.Text(), nullable=True),
       sa.Column('pinged', sa.DateTime(), nullable=False),
       sa.Column('author_id', sa.String(length=64), nullable=True),
       sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
       sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sources_name'), 'sources', ['name'], unique=False)
    op.create_index(op.f('ix_sources_pinged'), 'sources', ['pinged'], unique=False)
    op.create_table('annotations',
       sa.Column('id', sa.String(length=64), nullable=False),
       sa.Column('source_id', sa.String(length=64), nullable=True),
       sa.Column('passage', sa.Text(), nullable=False),
       sa.Column('notes', sa.Text(), nullable=True),
       sa.Column('created', sa.DateTime(), nullable=False),
       sa.Column('modified', sa.DateTime(), nullable=False),
       sa.Column('origin', sa.String(length=64), nullable=False),
       sa.Column('protected', sa.Boolean(), nullable=False),
       sa.Column('deleted', sa.Boolean(), nullable=True),
       sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ),
       sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_annotations_created'), 'annotations', ['created'], unique=False)
    op.create_index(op.f('ix_annotations_modified'), 'annotations', ['modified'], unique=False)
    op.create_table('annotation_collections',
       sa.Column('collection_id', sa.Integer(), nullable=False),
       sa.Column('annotation_id', sa.String(length=64), nullable=False),
       sa.ForeignKeyConstraint(['annotation_id'], ['annotations.id'], ),
       sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
       sa.PrimaryKeyConstraint('collection_id', 'annotation_id')
    )
    op.create_table('annotation_tags',
       sa.Column('tag_id', sa.Integer(), nullable=False),
       sa.Column('annotation_id', sa.String(length=64), nullable=False),
       sa.ForeignKeyConstraint(['annotation_id'], ['annotations.id'], ),
       sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
       sa.PrimaryKeyConstraint('tag_id', 'annotation_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('annotation_tags')
    op.drop_table('annotation_collections')
    op.drop_index(op.f('ix_annotations_modified'), table_name='annotations')
    op.drop_index(op.f('ix_annotations_created'), table_name='annotations')
    op.drop_table('annotations')
    op.drop_index(op.f('ix_sources_pinged'), table_name='sources')
    op.drop_index(op.f('ix_sources_name'), table_name='sources')
    op.drop_table('sources')
    op.drop_index(op.f('ix_users_api_key'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_tags_pinged'), table_name='tags')
    op.drop_index(op.f('ix_tags_name'), table_name='tags')
    op.drop_table('tags')
    op.drop_index(op.f('ix_collections_pinged'), table_name='collections')
    op.drop_index(op.f('ix_collections_name'), table_name='collections')
    op.drop_table('collections')
    op.drop_index(op.f('ix_authors_pinged'), table_name='authors')
    op.drop_index(op.f('ix_authors_name'), table_name='authors')
    op.drop_table('authors')
    # ### end Alembic commands ###
