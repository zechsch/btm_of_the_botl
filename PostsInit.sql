DROP TABLE ArchivedPosts;
DROP TABLE Posts;
Drop sequence "tid";

create sequence tid start 1;

CREATE TABLE Posts (

    PostID      integer PRIMARY KEY default nextval('tid'),
    Latitude    double precision  NOT NULL,
    Longitude   double precision  NOT NULL,
    Ts          timestamp without time zone NOT NULL default (now() at time zone 'utc'),
    Message     varchar(250) NOT NULL,
    ThreadId    integer,
    Rating      integer NOT NULL default 0,
    UserID      integer references "users"(user_id),
    Uts         timestamp without time zone NOT NULL default (now() at time zone 'utc'),
    ExpiredDate timestamp without time zone NOT NULL default (now() at time zone 'utc' + interval '12 hours')
);

CREATE TABLE ArchivedPosts (

    PostID      integer PRIMARY KEY,
    Latitude    double precision  NOT NULL,
    Longitude   double precision  NOT NULL,
    Ts          timestamp without time zone NOT NULL default (now() at time zone 'utc'),
    Message     varchar(250) NOT NULL,
    ThreadId    integer,
    Rating      integer NOT NULL,
    UserID      integer NOT NULL references "users"(user_id),
    Uts         timestamp without time zone NOT NULL default (now() at time zone 'utc'),
    ExpiredDate timestamp without time zone NOT NULL default (now() at time zone 'utc' + interval '12 hours')
);
