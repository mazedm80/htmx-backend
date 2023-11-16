-- dummy data of auth_group
INSERT INTO public.auth_group 
    (name) 
VALUES 
    ('super admin'),
    ('admin'),
    ('owner'),
    ('manager'),
    ('staff'),
    ('customer')
;

-- dummy data of users
INSERT INTO public.users 
    (email, name, dob, password, is_active)
VALUES
    ('super_admin@super_admin.com', 'super admin', '1990-01-01', 'superadmin123', true),
    ('admin@admin.com', 'admin', '1990-01-01', 'admin123', true),
    ('owner@owner.com', 'owner', '1990-01-01', 'owner123', true),
    ('manager@manager.com', 'manager', '1990-01-01', 'manager123', true),
    ('staff@staff.com', 'staff', '1990-01-01', 'staff123', true),
    ('customer@customer.com', 'customer', '1990-01-01', 'customer123', true)
;
-- dummy data of user_permissions
INSERT INTO public.user_permissions 
    (user_id, permission_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6)
;
-- dummy data for menu category
INSERT INTO public.menu_categories 
    (user_id, name, description, image)
VALUES
    (7, 'Burger', 'Beef Burger', 'https://pngfre.com/wp-content/uploads/Burger-43.png')