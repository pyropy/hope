"""users functions
Revision ID: dc0130a0b54b
Revises: 277259b72b52
Create Date: 2021-04-02 11:25:10.407333
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'dc0130a0b54b'
down_revision = '277259b72b52'
branch_labels = None
depends_on = None

def create_user_functions() -> None:
    # create new user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.create_user_function(
        i_full_name text, 
        i_username text, 
        i_email text, 
        i_salt text, 
        i_password text, 
        i_email_verified boolean default 'f',
        i_is_active boolean default 'f',
        i_is_superuser boolean default 'f',
        i_jwt_token text default null,
        i_confirmation_code varchar(6) default null)
    RETURNS TABLE (id int, full_name text, username text, email text, password text, salt text, confirmation_code varchar(6), jwt_token text)
    AS $$
    DECLARE 
        inserted_id int;
    BEGIN
        INSERT INTO users.users (
            full_name,
            username,
            email,
            email_verified,
            salt,
            password,
            is_active,
            is_superuser,
            jwt_token,
            confirmation_code)
        VALUES (
            i_full_name,
            i_username,
            i_email,
            i_email_verified,
            i_salt,
            i_password,
            i_is_active,
            i_is_superuser,
            i_jwt_token,
            i_confirmation_code) RETURNING users.users.id INTO inserted_id;
        RETURN QUERY (SELECT
            users.users.id, 
            users.users.full_name, 
            users.users.username, 
            users.users.email,
            users.users.password,
            users.users.salt,
            users.users.confirmation_code,
            users.users.jwt_token
            FROM users.users WHERE users.users.id = inserted_id);
    END $$ LANGUAGE plpgsql;
    """)
    # add grade to user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.add_grade_to_user_function(user_id int, grade_id int, days int)
    RETURNS VOID
    AS $$
    BEGIN
        INSERT INTO users.user_grades(user_fk, grade_fk, days_left) VALUES(user_id, grade_id, days);
    END $$ LANGUAGE plpgsql;
    """)
    # add subject to user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.add_subject_to_user_function(user_id int, subject_id int, days int)
    RETURNS VOID
    AS $$
    BEGIN 
        INSERT INTO users.user_subjects(user_fk, subject_fk, days_left) VALUES (user_id, subject_id, days);
    END $$ LANGUAGE plpgsql;
    """)

    # remove grade from user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.remove_grade_from_user_function(user_id int, grade_id int)
    RETURNS VOID
    AS $$ 
    BEGIN 
        DELETE FROM users.user_grades WHERE users.user_grades.user_fk = user_id AND users.user_grades.grade_fk = grade_id;
    END $$ LANGUAGE plpgsql;
    """)
    # remove subject from user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.remove_subject_from_user_function(user_id int, subject_id int)
    RETURNS VOID
    AS $$
    BEGIN
        DELETE FROM users.user_subjects WHERE users.user_subjects.user_fk = user_id AND users.user_subjects.subject_fk = subject_id;
    END $$ LANGUAGE plpgsql;
    """)

    # prolong grade subscription duration
    op.execute("""
    CREATE OR REPLACE FUNCTION users.prolong_grade_subscription(user_id int, grade_id int, days int)
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE users.user_grades SET
            days_left = days,
            updated_at = now() 
        WHERE users.user_grades.user_fk = user_id AND users.user_grades.grade_fk = grade_id;
    END $$ LANGUAGE plpgsql;
    """)
    # prolong subject subscription duration
    op.execute("""
    CREATE OR REPLACE FUNCTION users.prolong_subject_subscription(user_id int, subject_id int, days int)
    RETURNS VOID
    AS $$ 
    BEGIN 
        UPDATE users.user_subjects SET
            days_left = days,
            updated_at = now()
        WHERE users.user_subjects.user_fk = user_id AND users.user_subjects.subject_fk = subject_id;
    END $$ LANGUAGE plpgsql;
    """)

    # select all user available grades
    op.execute("""
    CREATE OR REPLACE FUNCTION users.select_all_user_available_grades(user_id int)
    RETURNS TABLE (grade_id int, created_at timestamp, updated_at timestamp)
    AS $$
    BEGIN
        RETURN QUERY (SELECT users.user_grades.grade_fk, users.user_grades.created_at, users.user_grades.updated_at FROM users.user_grades WHERE users.user_grades.user_fk = user_id);
    END $$ LANGUAGE plpgsql;
    """)
    # select all user available subjects
    op.execute("""
    CREATE OR REPLACE FUNCTION users.select_all_user_available_subjects(user_id int)
    RETURNS TABLE (subject_id int, created_at timestamp, updated_at timestamp)
    AS $$
    BEGIN 
        RETURN QUERY (SELECT users.user_subjects.subject_fk, users.user_subjects.created_at, users.user_subjects.updated_at FROM users.user_subjcts WHERE users.user_subjects.user_fk = user_id);
    END $$ LANGUAGE plpgsql;
    """)

    # decrement days left
    op.execute("""
    CREATE OR REPLACE FUNCTION users.decrement_days_left_count()
    RETURNS VOID
    AS $$
    BEGIN
        UPDATE users.user_grades SET
            days_left = days_left - 1;
        UPDATE users.subject_grades SET
            days_left = days_left - 1;
        SELECT delete_expired_subscriptions();
    END $$ LANGUAGE plpgsql;
    """)

    # delete expired subscriptions grades
    op.execute("""
    CREATE OR REPLACE FUNCTION users.delete_expired_subscriptions()
    RETURNS VOID
    AS $$
    BEGIN 
        DELETE FROM users.user_grades WHERE days_left < 0;
        DELETE FROM users.user_subjects WHERE days_left < 0;
    END $$ LANGUAGE plpgsql;
    """)

    # get user by email
    op.execute("""
    CREATE OR REPLACE FUNCTION users.get_user_by_email(i_email text)
    RETURNS TABLE (id int, full_name text, username text, email text, password text, salt text, jwt text, confirmation_code varchar(6), is_active boolean, email_verified boolean, is_superuser boolean)
    AS $$
    BEGIN 
            RETURN QUERY (SELECT
            users.users.id, 
            users.users.full_name, 
            users.users.username, 
            users.users.email,
            users.users.password,
            users.users.salt,
            users.users.jwt_token,
            users.users.confirmation_code,
            users.users.is_active,
            users.users.email_verified,
            users.users.is_superuser
            FROM users.users WHERE users.users.email = i_email);
    END $$ LANGUAGE plpgsql;
    """)

    # get user by username
    op.execute("""
    CREATE OR REPLACE FUNCTION users.get_user_by_username(i_username text)
    RETURNS TABLE (id int, full_name text, username text, email text, password text, salt text, jwt text, confirmation_code varchar(6), is_active boolean, email_verified boolean, is_superuser boolean)
    AS $$
    BEGIN
            RETURN QUERY (SELECT
            users.users.id, 
            users.users.full_name, 
            users.users.username, 
            users.users.email,
            users.users.password,
            users.users.salt,
            users.users.jwt_token,
            users.users.confirmation_code,
            users.users.is_active,
            users.users.email_verified,
            users.users.is_superuser
            FROM users.users WHERE users.users.username = i_username);
    END $$ LANGUAGE plpgsql;
    """)

def create_user_authentication_functions() -> None:
    # set confirmation code
    op.execute(
    """
    CREATE OR REPLACE FUNCTION users.set_confirmation_code(user_id int, i_confirmation varchar(6))
    RETURNS VOID
    AS $$
    BEGIN
        UPDATE users.users SET
            confirmation_code = i_confirmation
        WHERE users.users.id = user_id;
    END $$ LANGUAGE plpgsql;
    """)

    # set jwt token
    op.execute(
    """
    CREATE OR REPLACE FUNCTION users.set_jwt_token(user_id int, token text)
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE users.users SET
            jwt_token = token,
            is_active = 't'
        WHERE users.users.id = user_id;
    END $$ LANGUAGE plpgsql;
    """)

    # verify email
    op.execute(
    """
    CREATE OR REPLACE FUNCTION users.verify_email(user_id int)
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE users.users SET
            email_verified = 't'
        WHERE users.users.id = user_id;
    END $$ LANGUAGE plpgsql;
    """
    )


def delete_users_functions() -> None:
    functions = [
        'create_user_function',
        'add_grade_to_user_function',
        'add_subject_to_user_function',
        'remove_grade_from_user_function',
        'remove_subject_from_user_function',
        'prolong_grade_subscription',
        'prolong_subject_subscription',
        'select_all_user_available_grades',
        'select_all_user_available_subjects',
        'decrement_days_left_count',
        'delete_expired_subscriptions',
        'get_user_by_username',
        'get_user_by_email',
        'set_confirmation_code',
        'set_jwt_token',
        'verify_email',
        ]

    for function in functions:
        op.execute(f"DROP FUNCTION users.{function}")

def upgrade() -> None:
    create_user_functions()
    create_user_authentication_functions()

def downgrade() -> None:
    delete_users_functions()