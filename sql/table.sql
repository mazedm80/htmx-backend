-- Description: This file contains the SQL commands to create the tables in the database.
DROP USER IF EXISTS htmx;
CREATE USER htmx WITH
    NOSUPERUSER
    INHERIT
    CREATEDB
    LOGIN
    PASSWORD 'htmx123';

-- Database: pyhtmx
DROP DATABASE IF EXISTS pyhtmx;
CREATE DATABASE pyhtmx
    WITH 
    OWNER = htmx
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Grant permissions to htmx user
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO htmx;
-- User Table
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS public.users
(
    id SERIAL NOT NULL PRIMARY KEY,
    email text NOT NULL,
    name text NOT NULL,
    dob date NOT NULL,
    password text NOT NULL,
    is_active boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);
CREATE INDEX IF NOT EXISTS users_email_idx ON public.users USING btree (email);

-- Permission Table
DROP TABLE IF EXISTS public.auth_group;
CREATE TABLE IF NOT EXISTS public.auth_group
(
    id SERIAL NOT NULL PRIMARY KEY,
    name text NOT NULL
);

-- User Permission Table
DROP TABLE IF EXISTS public.user_permissions;
CREATE TABLE IF NOT EXISTS public.user_permissions
(
    id SERIAL NOT NULL,
    user_id integer NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    permission_id integer NOT NULL REFERENCES public.auth_group(id) ON DELETE CASCADE,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    PRIMARY KEY (user_id, permission_id)
);
CREATE UNIQUE INDEX IF NOT EXISTS user_permissions_user_id_idx ON public.user_permissions USING btree (user_id);

-- Restaurant Table
DROP TABLE IF EXISTS public.restaurants;
CREATE TABLE IF NOT EXISTS public.restaurants
(
    id SERIAL NOT NULL PRIMARY KEY,
    name text NOT NULL,
    address text NOT NULL,
    phone text NOT NULL,
    email text NOT NULL,
    website text NOT NULL,
    image text NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);
CREATE INDEX IF NOT EXISTS restaurants_name_idx ON public.restaurants USING btree (name);

-- Restaurant access Table
DROP TABLE IF EXISTS public.restaurant_access;
CREATE TABLE IF NOT EXISTS public.restaurant_access
(
    id SERIAL NOT NULL,
    user_id integer NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    restaurant_id integer NOT NULL REFERENCES public.restaurants(id) ON DELETE CASCADE,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    PRIMARY KEY (user_id, restaurant_id)
);
CREATE INDEX IF NOT EXISTS restaurant_access_user_id_idx ON public.restaurant_access USING btree (user_id);

-- Restaurant table
DROP TABLE IF EXISTS public.restaurant_tables;
CREATE TABLE IF NOT EXISTS public.restaurant_tables
(
    id SERIAL NOT NULL,
    restaurant_id integer NOT NULL REFERENCES public.restaurants(id) ON DELETE CASCADE,
    table_number integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    PRIMARY KEY (restaurant_id, table_number)
);
CREATE INDEX IF NOT EXISTS restaurant_tables_restaurant_id_idx ON public.restaurant_tables USING btree (restaurant_id);

-- Menu categories table
DROP TABLE IF EXISTS public.menu_categories;
CREATE TABLE IF NOT EXISTS public.menu_categories
(
    id SERIAL NOT NULL PRIMARY KEY,
    user_id integer NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    name text NOT NULL,
    description text,
    image text NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);
CREATE INDEX IF NOT EXISTS menu_categories_user_id_idx ON public.menu_categories USING btree (user_id);

-- Spice level Enum
DROP TYPE IF EXISTS spice_level;
CREATE TYPE spice_level AS ENUM ('mild', 'medium', 'hot', 'extra');

-- Menu items table
DROP TABLE IF EXISTS public.menu_items;
CREATE TABLE IF NOT EXISTS public.menu_items
(
    id SERIAL NOT NULL PRIMARY KEY,
    user_id integer NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    menu_category_id integer NOT NULL REFERENCES public.menu_categories(id) ON DELETE CASCADE,
    name text NOT NULL,
    description text,
    price real NOT NULL,
    making_time real NOT NULL,
    image text NOT NULL,
    status boolean DEFAULT true,
    vegetarian boolean DEFAULT false,
    vegan boolean DEFAULT false,
    gluten_free boolean DEFAULT false,
    spice_level spice_level NOT NULL DEFAULT 'mild',
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);
CREATE INDEX IF NOT EXISTS menu_items_user_id_idx ON public.menu_items USING btree (user_id);

-- Order status Enum
DROP TYPE IF EXISTS order_status;
CREATE TYPE order_status AS ENUM ('pending', 'accepted', 'rejected', 'completed');
-- Order table
DROP TABLE IF EXISTS public.orders;
CREATE TABLE IF NOT EXISTS public.orders
(
    id SERIAL NOT NULL PRIMARY KEY,
    
    restaurant_id integer NOT NULL REFERENCES public.restaurants(id) ON DELETE CASCADE,
    table_number integer NOT NULL,
    status order_status NOT NULL DEFAULT 'pending',
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);