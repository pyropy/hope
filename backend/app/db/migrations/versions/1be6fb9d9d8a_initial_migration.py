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

def create_stored_procedures_insert() -> None:
    # grades insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION insert_grade(varchar(20), varchar(20), text, text)
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.grade (name_en, name_ru, background_key, background) VALUES ($1, $2, $3, $4) 
        RETURNING private.grade.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # subject insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION insert_subject(int, varchar(20), varchar(20), text, text)
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.subject (fk, name_en, name_ru, background_key, background) VALUES ($1, $2, $3, $4, $5) RETURNING private.subject.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # branch insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION insert_branch(int, varchar(20), varchar(20), text, text)
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.branch (fk, name_en, name_ru, background_key, background) VALUES ($1, $2, $3, $4, $5) RETURNING private.branch.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # lecture insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION insert_lecture(int, varchar(20), varchar(20), text, text, text)
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.lecture (fk, name_en, name_ru, description, background_key, background) VALUES ($1, $2, $3, $4, $5) RETURNING private.lecture.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # video insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION insert_video(int, varchar(20), text, text, text)
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text, key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.video (fk, name_ru, description, key, url) VALUES ($1, $2, $3, $4, $5) RETURNING private.video.fk INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.video WHERE private.video.fk = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # book insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION insert_book(int, varchar(20), text, text, text)
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text, key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.book (fk, name_ru, description, key, url) VALUES ($1, $2, $3, $4, $5) RETURNING private.book.fk INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.book WHERE private.book.fk = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # game insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION insert_game(int, varchar(20), text, text)
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.game (fk, name_ru, description, url) VALUES ($1, $2, $3, $4) RETURNING private.game.fk INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.game WHERE private.game.fk = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

    # theory insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION insert_theory(int, varchar(20), text, text)
        RETURNS TABLE (id int, name_ru varchar(20), description text, key text)
        AS $$
        DECLARE
        inserted_id int;
        BEGIN
        INSERT INTO private.theory (fk, name_ru, description, key) VALUES ($1, $2, $3, $4) RETURNING private.theory.fk INTO inserted_id;
        RETURN QUERY (SELECT * FROM private.theory WHERE private.theory.fk = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)
    # theory images insert function
    # NOTE: Try inserting for error!
    op.execute("""
    CREATE OR REPLACE FUNCTION insert_theory_image(text, text, text[], text[])
        RETURNS TABLE ("order" int, url text, key text)
        AS $$
        DECLARE 
            orders INT[];
            fks INT[];
        BEGIN
        fks = string_to_array($1,',');
        orders = string_to_array($2, ',');
        INSERT INTO private.theory_image (fk, "order", url, key)
        SELECT unnest(fks), unnest(orders), unnest($3), unnest($4);
        RETURN QUERY (SELECT private.theory_image."order", private.theory_image.url, private.theory_image.key FROM private.theory_image WHERE private.theory_image.fk = $1[0]);
        END $$ LANGUAGE plpgsql;
    """)
    # theory images insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION insert_theory_audio(text, text, text[], text[])
        RETURNS TABLE ("order" int, url text, key text)
        AS $$
        DECLARE 
            orders INT[];
            fks INT[];
        BEGIN
        fks = string_to_array($1,',');
        orders = string_to_array($2,',');
        INSERT INTO private.theory_audio (fk, "order", url, key)
        SELECT unnest(fks), unnest(orders), unnest($3), unnest($4);
        RETURN QUERY (SELECT private.theory_audio."order", private.theory_audio.url, private.theory_audio.key FROM private.theory_audio WHERE private.theory_audio.fk = $1[0]);
        END $$ LANGUAGE plpgsql;
    """)

def create_stored_procedures_select() -> None:
    # grades select functions
    op.execute("""
    CREATE OR REPLACE FUNCTION select_grades_by_ids(text)
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        DECLARE 
            ids INT[];
        BEGIN
        ids = string_to_array($1,',');
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.id = ANY(ids));
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION select_all_grades()
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.grade);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
     CREATE OR REPLACE FUNCTION select_grade_by_name(text)
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.grade WHERE private.grade.name_en = $1);
        END $$ LANGUAGE plpgsql;
    """)

    # subject select functions
    op.execute("""
    CREATE OR REPLACE FUNCTION select_subjects_by_ids(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        DECLARE 
            ids INT[];
        BEGIN
        ids = string_to_array($1,',');
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.id = ANY(ids) AND private.subject.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION select_all_subjects(int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION select_subject_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.subject WHERE private.subject.name_en = $1 AND private.subject.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)

    # branch select functions
    op.execute("""
    CREATE OR REPLACE FUNCTION select_all_branches(int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION select_branch_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.branch WHERE private.branch.name_en = $1 AND private.branch.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)

    # lecture select function
    op.execute("""
    CREATE OR REPLACE FUNCTION select_all_lectures(int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), description text, background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION select_lecture_by_name(text, int)
        RETURNS TABLE (id int, fk int, name_en varchar(20), name_ru varchar(20), description text, background text, background_key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.lecture WHERE private.lecture.name_en = $1 AND private.lecture.fk = $2);
        END $$ LANGUAGE plpgsql;
    """)

    # theory
    op.execute("""
    CREATE OR REPLACE FUNCTION select_theory(int)
        RETURNS TABLE (id int, name_ru varchar(20), description text, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.theory WHERE private.theory.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    # thoery images
    op.execute("""
    CREATE OR REPLACE FUNCTION select_theory_images(int)
        RETURNS TABLE (url varchar(20), "order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT url, "order", key FROM private.theory_image WHERE private.theory_image.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    # theory audio
    op.execute("""
    CREATE OR REPLACE FUNCTION select_theory_audio(int)
        RETURNS TABLE (url varchar(20), "order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT url, "order", key FROM private.theory_audio WHERE private.theory_audio.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    
    # practice
    op.execute("""
    CREATE OR REPLACE FUNCTION select_practice(int)
        RETURNS TABLE (id int, name_ru varchar(20), description text, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.practice WHERE private.practice.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    # practice images
    op.execute("""
    CREATE OR REPLACE FUNCTION select_practice_images(int)
        RETURNS TABLE (url varchar(20), "order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT url, "order", key FROM private.practice_image WHERE private.practice_image.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    # practice audio
    op.execute("""
    CREATE OR REPLACE FUNCTION select_practice_audio(int)
        RETURNS TABLE (url varchar(20), "order" int, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT url, "order", key FROM private.practice_audio WHERE private.practice_audio.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    # video
    op.execute("""
    CREATE OR REPLACE FUNCTION select_video(int)
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.video WHERE private.video.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)
    
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION select_book(int)
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text, key text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.book WHERE private.book.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

    # game
    op.execute("""
    CREATE OR REPLACE FUNCTION select_game(int)
        RETURNS TABLE (id int, url text, name_ru varchar(20), description text)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.game WHERE private.game.fk = $1);
        END $$ LANGUAGE plpgsql;
    """)

def create_private_tables() -> None:
    # grades table
    op.create_table(
        "grade", 
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name_en", sa.String(20), nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("background", sa.Text, nullable=False),
        sa.Column("background_key", sa.Text, nullable=False),
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
        sa.Column("background", sa.Text, nullable=False),
        sa.Column("background_key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.grade.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk', 'name_en'),
        schema="private"    
    )

    # branches table
    op.create_table(
        "branch",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fk", sa.Integer, nullable=False),
        sa.Column("name_en", sa.String(20), nullable=False),
        sa.Column("name_ru", sa.String(20), nullable=False),
        sa.Column("background", sa.Text, nullable=False),
        sa.Column("background_key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.subject.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk', 'name_en'),
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
        sa.Column("background", sa.Text, nullable=False),
        sa.Column("background_key", sa.Text, nullable=False),
        sa.ForeignKeyConstraint(['fk'], ['private.branch.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.UniqueConstraint('fk', 'name_en'),
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
        sa.Column("key", sa.Text, nullable=True),
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
        sa.Column("key", sa.Text, nullable=False),
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
        sa.Column("key", sa.Text, nullable=False),
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
        sa.Column("key", sa.Text, nullable=False),
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
        sa.Column("key", sa.Text, nullable=False),
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

    create_stored_procedures_select()


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