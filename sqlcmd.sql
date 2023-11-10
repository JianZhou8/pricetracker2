

select * from userauth_tracklist ;
delete from userauth_tracklist ;
select * from auth_user;
UPDATE auth_user SET email = 'zhou0214@algonquinlive.com' WHERE id = 1;


INSERT INTO userauth_tracklist (user_id, number, url, current_price, target_price, check_frequency, last_check_time, enable_auto_monitoring)
VALUES
    (1, 1, 'https://example.com/1', 10, 10.0, 30, '2023-10-27 12:00:00', 1),
    (1, 2, 'https://example.com/2', 20, 15.0, 15, '2023-10-27 13:30:00', 0),
    (1, 3, 'https://example.com/3', 30, 20.0, 60, '2023-10-27 15:15:00', 1),
    (2, 4, 'https://example.com/4', 40, 25.0, 45, '2023-10-27 16:45:00', 0),
    (2, 5, 'https://example.com/5', 50, 30.0, 10, '2023-10-27 18:20:00', 1);
