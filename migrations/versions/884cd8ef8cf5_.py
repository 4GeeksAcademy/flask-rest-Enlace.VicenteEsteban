"""empty message

Revision ID: 884cd8ef8cf5
Revises: c239ebfb34c8
Create Date: 2024-07-23 16:38:45.014434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '884cd8ef8cf5'
down_revision = 'c239ebfb34c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.drop_constraint('planet_climate_key', type_='unique')
        batch_op.drop_constraint('planet_created_key', type_='unique')
        batch_op.drop_constraint('planet_diameter_key', type_='unique')
        batch_op.drop_constraint('planet_edited_key', type_='unique')
        batch_op.drop_constraint('planet_gravity_key', type_='unique')
        batch_op.drop_constraint('planet_name_key', type_='unique')
        batch_op.drop_constraint('planet_orbital_period_key', type_='unique')
        batch_op.drop_constraint('planet_population_key', type_='unique')
        batch_op.drop_constraint('planet_rotation_period_key', type_='unique')
        batch_op.drop_constraint('planet_surface_water_key', type_='unique')
        batch_op.drop_constraint('planet_terrain_key', type_='unique')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('user_first_name_key', type_='unique')
        batch_op.drop_constraint('user_last_name_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint('user_last_name_key', ['last_name'])
        batch_op.create_unique_constraint('user_first_name_key', ['first_name'])

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.create_unique_constraint('planet_terrain_key', ['terrain'])
        batch_op.create_unique_constraint('planet_surface_water_key', ['surface_water'])
        batch_op.create_unique_constraint('planet_rotation_period_key', ['rotation_period'])
        batch_op.create_unique_constraint('planet_population_key', ['population'])
        batch_op.create_unique_constraint('planet_orbital_period_key', ['orbital_period'])
        batch_op.create_unique_constraint('planet_name_key', ['name'])
        batch_op.create_unique_constraint('planet_gravity_key', ['gravity'])
        batch_op.create_unique_constraint('planet_edited_key', ['edited'])
        batch_op.create_unique_constraint('planet_diameter_key', ['diameter'])
        batch_op.create_unique_constraint('planet_created_key', ['created'])
        batch_op.create_unique_constraint('planet_climate_key', ['climate'])

    # ### end Alembic commands ###