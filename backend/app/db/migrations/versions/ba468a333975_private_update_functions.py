"""private update functions
Revision ID: ba468a333975
Revises: 1be6fb9d9d8a
Create Date: 2021-03-27 15:36:51.882562
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'ba468a333975'
down_revision = '1be6fb9d9d8a'
branch_labels = None
depends_on = None

def create_stored_procedures_update() -> None:
    # update grade functions
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_grade(int, varchar(20), text, text)
        RETURNS TABLE (id int, name_en varchar(20), name_ru varchar(20), background text, background_key text)
        AS $$
        BEGIN
        UPDATE private.grade SET 
        private.grade.name_ru = COALESCE($2, private.grade.name_ru),
        private.grade.background = COALESCE($3, private.grade.background),
        private.grade.background_key = COALESCE($4, private.grade.background_key)
        WHERE private.grade.id = $1;
        RETURN QUERY (SELECT * FROM private.grade WHERE id = $1);
        END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_grade_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.grade SET
            background = $2[index] 
            WHERE background_key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)

    # subject
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_subject_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.subject SET
            background = $2[index] 
            WHERE background_key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # branch
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_branch_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.branch SET
            background = $2[index] 
            WHERE background_key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # lecture
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_lecture_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.lecture SET
            background = $2[index] 
            WHERE background_key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # theory

    # theory images
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_theory_image_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.theory_image SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # theory audio
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_theory_audio_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.theory_audio SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # practice

    # practice images
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_practice_image_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.practice_image SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)
    # practice audio
    op.execute("""
    CREATE OR REPLACE FUNCTION private.update_practice_audio_links(text[], text[])
        RETURNS VOID
        AS $$
        BEGIN
        FOR index IN 1 .. array_upper($1, 1)
        LOOP
            UPDATE private.practice_audio SET
            url = $2[index] 
            WHERE key = $1[index];
        END LOOP;
        END $$ LANGUAGE plpgsql;
    """)

def drop_stored_procedures() -> None:
    procedures = [
        'update_grade',
        'update_grade_links',
        'update_subject_links',
        'update_branch_links',
        'update_lecture_links',
        'update_practice_image_links',
        'update_practice_audio_links',
        'update_theory_image_links',
        'update_theory_audio_links',
    ]

    for procedure in procedures:
        op.execute(f"DROP FUNCTION private.{procedure}")

def upgrade() -> None:
    create_stored_procedures_update()

def downgrade() -> None:
    drop_stored_procedures()