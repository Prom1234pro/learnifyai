"""First Migrations

Revision ID: ace8f144bc95
Revises: 
Create Date: 2024-06-03 21:35:17.810860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ace8f144bc95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('max_no_users', sa.Integer(), nullable=True),
    sa.Column('current_no_users', sa.Integer(), nullable=True),
    sa.Column('group_admin_id', sa.String(length=36), nullable=True),
    sa.Column('activated', sa.Boolean(), nullable=True),
    sa.Column('school', sa.String(length=120), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=True),
    sa.Column('group_key', sa.String(length=120), nullable=True),
    sa.Column('pass_key', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('is_logged_in', sa.Boolean(), nullable=True),
    sa.Column('email_verified', sa.Boolean(), nullable=True),
    sa.Column('last_activity_time', sa.DateTime(), nullable=True),
    sa.Column('verification_token', sa.String(length=60), nullable=True),
    sa.Column('is_premium_user', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('course',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('course_name', sa.String(length=125), nullable=True),
    sa.Column('url', sa.String(length=125), nullable=True),
    sa.Column('no_of_topics', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups',
    sa.Column('group_id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('group_id', 'user_id')
    )
    op.create_table('topic',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('course_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quiz',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('topic_id', sa.String(length=36), nullable=False),
    sa.Column('type_', sa.String(length=60), nullable=True),
    sa.Column('question_text', sa.Text(), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('hint', sa.Text(), nullable=True),
    sa.Column('course_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('summary',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('keynote', sa.Text(), nullable=True),
    sa.Column('topic_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('option',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('option_text', sa.Text(), nullable=True),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('option')
    op.drop_table('summary')
    op.drop_table('quiz')
    op.drop_table('topic')
    op.drop_table('groups')
    op.drop_table('course')
    op.drop_table('user')
    op.drop_table('group')
    # ### end Alembic commands ###
