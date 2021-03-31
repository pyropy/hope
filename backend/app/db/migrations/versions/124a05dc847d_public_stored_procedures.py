"""public stored procedures
Revision ID: 124a05dc847d
Revises: 6e7bb8073b9f
Create Date: 2021-03-31 08:36:12.946707
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '124a05dc847d'
down_revision = '6e7bb8073b9f'
branch_labels = None
depends_on = None

def create_insert_public_procedures() -> None:
    # game
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_game(varchar(100), text, text)
        RETURNS TABLE (name_ru varchar(100), url text, description text)
        AS $$
        BEGIN
        DELETE FROM public.game;
        INSERT INTO public.game (name_ru, url, description) VALUES ($1, $2, $3);
        RETURN QUERY (SELECT * FROM public.game);
        END $$ LANGUAGE plpgsql;
    """)
    # video
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_video(varchar(100), text, text)
        RETURNS TABLE (name_ru varchar(100), url text, description text)
        AS $$
        BEGIN
        DELETE FROM public.video;
        INSERT INTO public.video (name_ru, url, description) VALUES ($1, $2, $3);
        RETURN QUERY (SELECT * FROM public.video);
        END $$ LANGUAGE plpgsql;
    """)
    # book
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_book(varchar(100), text, text, text)
        RETURNS TABLE (name_ru varchar(100), url text, description text, key text)
        AS $$
        BEGIN
        DELETE FROM public.book;
        INSERT INTO public.book (name_ru, url, description, key) VALUES ($1, $2, $3, $4);
        RETURN QUERY (SELECT * FROM public.book);
        END $$ LANGUAGE plpgsql;
    """)
    # practice
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_practice(varchar(100), text, text)
        RETURNS TABLE (name_ru varchar(100), description text, key text)
        AS $$
        BEGIN
        DELETE FROM public.practice;
        INSERT INTO public.practice (name_ru, description, key) VALUES ($1, $2, $3);
        RETURN QUERY (SELECT * FROM public.practice);
        END $$ LANGUAGE plpgsql;
    """)
    # theory
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_theory(varchar(100), text, text)
        RETURNS TABLE (name_ru varchar(100), description text, key text)
        AS $$
        BEGIN
        DELETE FROM public.theory;
        INSERT INTO public.theory (name_ru, description, key) VALUES ($1, $2, $3);
        RETURN QUERY (SELECT * FROM public.theory);
        END $$ LANGUAGE plpgsql;
    """)

     # theory images insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_theory_image(int[], text[], text[])
        RETURNS TABLE ("order" int, url text, key text)
        AS $$
        BEGIN
        DELETE FROM public.theory_image;
        INSERT INTO public.theory_image ("order", url, key)
        SELECT unnest($1), unnest($2), unnest($3);
        RETURN QUERY (SELECT public.theory_image."order", public.theory_image.url, public.theory_image.key FROM public.theory_image);
        END $$ LANGUAGE plpgsql;
    """)

    # theory audio insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_theory_audio(int[], text[], text[])
        RETURNS TABLE ("order" int, url text, key text)
        AS $$
        BEGIN
        DELETE FROM public.theory_audio;
        INSERT INTO private.theory_audio ("order", url, key)
        SELECT unnest($1), unnest($2), unnest($3);
        RETURN QUERY (SELECT public.theory_audio."order", public.theory_audio.url, public.theory_audio.key FROM public.theory_audio);
        END $$ LANGUAGE plpgsql;
    """)

    # practice images insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_practice_image(int[], text[], text[])
        RETURNS TABLE ("order" int, url text, key text)
        AS $$
        BEGIN
        DELETE FROM public.practice_image;
        INSERT INTO public.practice_image ("order", url, key)
        SELECT unnest($1), unnest($2), unnest($3);
        RETURN QUERY (SELECT public.practice_image."order", public.practice_image.url, public.practice_image.key FROM public.practice_image);
        END $$ LANGUAGE plpgsql;
    """)
    # practice audio insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_practice_audio(int[], text[], text[])
        RETURNS TABLE ("order" int, url text, key text)
        AS $$
        BEGIN
        DELETE FROM public.practice_audio;
        INSERT INTO public.practice_audio ("order", url, key)
        SELECT unnest($1), unnest($2), unnest($3);
        RETURN QUERY (SELECT public.practice_audio."order", public.practice_audio.url, public.practice_audio.key FROM public.practice_audio);
        END $$ LANGUAGE plpgsql;
    """)

    # about us insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_about_us(int, text, text, text)
        RETURNS TABLE ("order" int, title text, description text, svg text)
        AS $$
        DECLARE
            inserted_id int;
        BEGIN
        INSERT INTO public.about_us ("order", title, description, svg) VALUES ($1, $2, $3, $4) RETURNING public.about_us.order INTO inserted_id;
        RETURN QUERY (SELECT * FROM public.about_us WHERE public.about_us.order = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)
    # faq insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_faq(text, text)
        RETURNS TABLE (id int, question text, answer text)
        AS $$
        DECLARE
            inserted_id int;
        BEGIN
        INSERT INTO public.faq (question, answer) VALUES ($1, $2) RETURNING public.faq.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM public.faq WHERE public.faq.id = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)
    # instruction insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_instruction(int, text, text)
        RETURNS TABLE ("order" int, title text, description text)
        AS $$
        DECLARE
            inserted_id int;
        BEGIN
        INSERT INTO public.instruction ("order", title, description) VALUES ($1, $2, $3) RETURNING public.instruction.order INTO inserted_id;
        RETURN QUERY (SELECT * FROM public.instruction WHERE public.instruction.order = inserted_id);
        END $$ LANGUAGE plpgsql;
    """)

def create_select_public_procedures() -> None:
    pass

def create_update_public_procedures() -> None:
    pass

def create_delete_public_procedures() -> None:
    pass


def drop_public_procedures() -> None:
    procedures = [
        'insert_practice_audio',
        'insert_practice_image',
        'insert_theory_audio',
        'insert_theory_image',
        'insert_theory',
        'insert_practice',
        'insert_book',
        'insert_video',
        'insert_game',
        'insert_about_us',
        'insert_faq',
        'insert_instruction',
    ]

    for proc in procedures:
        op.execute(f"DROP FUNCTION public.{proc}")


def upgrade() -> None:
    create_insert_public_procedures()
    create_select_public_procedures()
    create_update_public_procedures()
    create_delete_public_procedures()

def downgrade() -> None:
    drop_public_procedures()