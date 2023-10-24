-- User Table
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS public.users
(
    id SERIAL NOT NULL PRIMARY KEY,
    email text NOT NULL,
    name text NOT NULL,
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
