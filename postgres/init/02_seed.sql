-- NAS kaydı (FreeRADIUS'un kendisi)
INSERT INTO nas (nasname, shortname, secret, description)
VALUES ('127.0.0.1', 'localhost', 'testing123', 'Local FreeRADIUS test client')
ON CONFLICT DO NOTHING;

-- Admin kullanıcısı (şifre: Admin2026!)
INSERT INTO radcheck (username, attribute, op, value)
VALUES ('admin', 'Cleartext-Password', ':=', 'Admin2026!')
ON CONFLICT DO NOTHING;

-- Employee kullanıcısı (şifre: Emp2026!)
INSERT INTO radcheck (username, attribute, op, value)
VALUES ('employee1', 'Cleartext-Password', ':=', 'Emp2026!')
ON CONFLICT DO NOTHING;

-- Guest kullanıcısı (şifre: Guest2026!)
INSERT INTO radcheck (username, attribute, op, value)
VALUES ('guest1', 'Cleartext-Password', ':=', 'Guest2026!')
ON CONFLICT DO NOTHING;

-- MAB cihazı (yazıcı MAC adresi)
INSERT INTO radcheck (username, attribute, op, value)
VALUES ('aa:bb:cc:dd:ee:ff', 'Cleartext-Password', ':=', 'aa:bb:cc:dd:ee:ff')
ON CONFLICT DO NOTHING;

-- Kullanıcı-grup atamaları
INSERT INTO radusergroup (username, groupname, priority) VALUES
('admin',             'admin',    1),
('employee1',         'employee', 1),
('guest1',            'guest',    1),
('aa:bb:cc:dd:ee:ff', 'devices',  1)
ON CONFLICT DO NOTHING;

-- Grup VLAN atamaları
-- Admin -> VLAN 10
INSERT INTO radgroupreply (groupname, attribute, op, value) VALUES
('admin', 'Tunnel-Type',             ':=', '13'),
('admin', 'Tunnel-Medium-Type',      ':=', '6'),
('admin', 'Tunnel-Private-Group-Id', ':=', '10');

-- Employee -> VLAN 20
INSERT INTO radgroupreply (groupname, attribute, op, value) VALUES
('employee', 'Tunnel-Type',             ':=', '13'),
('employee', 'Tunnel-Medium-Type',      ':=', '6'),
('employee', 'Tunnel-Private-Group-Id', ':=', '20');

-- Guest -> VLAN 30
INSERT INTO radgroupreply (groupname, attribute, op, value) VALUES
('guest', 'Tunnel-Type',             ':=', '13'),
('guest', 'Tunnel-Medium-Type',      ':=', '6'),
('guest', 'Tunnel-Private-Group-Id', ':=', '30');

-- Devices (MAB) -> VLAN 40
INSERT INTO radgroupreply (groupname, attribute, op, value) VALUES
('devices', 'Tunnel-Type',             ':=', '13'),
('devices', 'Tunnel-Medium-Type',      ':=', '6'),
('devices', 'Tunnel-Private-Group-Id', ':=', '40');
