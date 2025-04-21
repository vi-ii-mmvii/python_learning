CREATE OR REPLACE FUNCTION search_phonebook(p_pattern text)
RETURNS TABLE(id INTEGER, name VARCHAR(30), surname VARCHAR(30), phone VARCHAR(30))
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.surname, p.phone
    FROM phonebook p
    WHERE p.name ILIKE '%' || p_pattern || '%'
       OR p.surname ILIKE '%' || p_pattern || '%'
       OR p.phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE phone = p_phone) THEN
        UPDATE phonebook
        SET name = p_name,
            surname = p_surname
        WHERE phone = p_phone;
    ELSE
        INSERT INTO phonebook(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION get_paginated_phonebook(limit_num INT, offset_num INT)
RETURNS TABLE(id INT, name VARCHAR, surname VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    ORDER BY id
    LIMIT limit_num OFFSET offset_num;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(p_value TEXT)
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value OR surname = p_value OR phone = p_value;
END;
$$ LANGUAGE plpgsql;

