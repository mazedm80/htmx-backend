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
    (email, name, password, is_active)
VALUES
    ('super_admin@super_admin.com', 'super admin', 'super_admin', true),
    ('admin@admin.com', 'admin', 'admin', true),
    ('owner@owner.com', 'owner', 'owner', true),
    ('manager@manager.com', 'manager', 'manager', true),
    ('staff@staff.com', 'staff', 'staff', true),
    ('customer@customer.com', 'customer', 'customer', true)
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