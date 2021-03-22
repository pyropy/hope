"""Initial migration
Revision ID: 1be6fb9d9d8a
Revises: 
Create Date: 2021-03-21 13:33:39.373009
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '1be6fb9d9d8a'
down_revision = None
branch_labels = None
depends_on = None

def create_private_tables() -> None:
    # grades table
    op.create_table(
        "grade", 
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name_en", sa.String(20), nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("background", sa.Text, nullable=True),
        sa.UniqueConstraint('name_en'),
        schema="private"
    )

    # subjects table
    op.create_table(
        "subject",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("name_en", sa.String(20), nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("background", sa.Text, nullable=True),
        sa.ForeignKeyConstraint(['fk'], ['private.grade.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('name_en'),
        schema="private"    
    )

    # branches table
    op.create_table(
        "branch",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("name_en", sa.String(20), nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("background", sa.Text, nullable=True),
        sa.ForeignKeyConstraint(['fk'], ['private.subject.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('name_en'),
        schema="private"    
    )

    # lectures table
    op.create_table(
        "lecture",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("name_en", sa.String(20), nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("background", sa.Text, nullable=True),
        sa.ForeignKeyConstraint(['fk'], ['private.branch.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('name_en'),
        schema="private"    
    )

    # material tables
    # video
    op.create_table(
        "video",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.lecture.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk'),
        schema="private"    
    )
    # game
    op.create_table(
        "game",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.lecture.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk'),
        schema="private"    
    )
    # book
    op.create_table(
        "book",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.lecture.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk'),
        schema="private"    
    )
    # theory
    op.create_table(
        "theory",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.lecture.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk'),
        schema="private"    
    )
    # practice
    op.create_table(
        "practice",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.lecture.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk'),
        schema="private"    
    )
    # theory images
    op.create_table(
        "theory_image",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.theory.fk'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint("fk", "order"),
        schema="private"
    )    
    # theory audio
    op.create_table(
        "theory_audio",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.theory.fk'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint("fk", "order"),
        schema="private"
    )    
    # practice images
    op.create_table(
        "practice_image",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.practice.fk'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint("fk", "order"),
        schema="private"
    )    
    # practice audio
    op.create_table(
        "practice_audio",
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.practice.fk'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint("fk", "order"),
        schema="private"
    )    
    # timestamp
    op.create_table(
        "timestamp",
        sa.Column("last_update",  sa.TIMESTAMP(timezone=True),server_default=sa.func.now(), nullable=False),
        sa.Column("is_updating", sa.Boolean, nullable=False),
        schema="private",
    )

    op.execute("""
        CREATE OR REPLACE FUNCTION update_timestamp_function()
            RETURNS TRIGGER AS
        $$
        BEGIN
        IF NEW.is_updating = 'f' THEN
            RAISE NOTICE 'SHOULD UPDATE';
            UPDATE private.timestamp
            SET last_update = now();
            RETURN NEW;
        ELSE
            RAISE NOTICE 'SHOULDNT UPDATE';
            RETURN NEW;
        END IF;
        END;
        $$ language 'plpgsql';

    """)

    op.execute("""
        CREATE TRIGGER update_timestamp
        AFTER UPDATE OF is_updating ON private.timestamp 
        FOR EACH ROW
        EXECUTE PROCEDURE update_timestamp_function()
    """)



def drop_private_tables() -> None:
    op.drop_table("theory_image", schema="private")
    op.drop_table("theory_audio", schema="private")
    op.drop_table("practice_image", schema="private")
    op.drop_table("practice_audio", schema="private")
    op.drop_table("practice", schema="private")
    op.drop_table("theory", schema="private")
    op.drop_table("book", schema="private")
    op.drop_table("game", schema="private")
    op.drop_table("video", schema="private")
    op.drop_table("lecture", schema="private")
    op.drop_table("branch", schema="private")
    op.drop_table("subject", schema="private")
    op.drop_table("grade", schema="private")
    op.drop_table('timestamp', schema='private')

def upgrade() -> None:
    create_private_tables()


def downgrade() -> None:
    drop_private_tables()