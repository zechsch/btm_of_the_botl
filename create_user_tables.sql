drop table users cascade;
drop table blacklist;
drop sequence uid;

create sequence uid start 101 cache 20;
    
create table users
    (
        user_id Integer not null default nextval('uid'),
        username varchar(8),
        user_passwrod varchar(16),
        user_device_id varchar(32) not null,
        user_karma Integer,
        user_photo varchar(32),
        user_phone varchar(10) not null,
        constraint userpk primary key (user_id)
    );

create table blacklist
    (
        blacklist_user_id Integer not null,
        blacklist_device_id varchar(32) not null,
        blacklist_phone varchar(10) not null,
        blacklist_penalty varchar(10) not null,
        blacklist_created timestamp not null,
        constraint blklsitpk primary key (blacklist_user_id),
        constraint userfk foreign key (blacklist_user_id) references users
    );
