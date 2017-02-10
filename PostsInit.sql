DROP TABLE "ArchivedPost";
DROP TABLE "Post";

CREATE TABLE "Post" (

    PostID      integer PRIMARY KEY,
    Latitude    double precision  NOT NULL,
    Longitude   double precision  NOT NULL,
    Date        date NOT NULL,
    Time        time NOT NULL,
    Message     varchar(250) NOT NULL,
    ThreadId    integer references "Post"(PostID),
    Rating      integer NOT NULL,
    UserID      integer NOT NULL references "users"(user_id),
    UpdatedDate date NOT NULL,
    UpdatedTime time NOT NULL,
    ExpiredDate date NOT NULL
);

CREATE TABLE "ArchivedPost" (

    PostID      integer PRIMARY KEY,
    Latitude    double precision  NOT NULL,
    Longitude   double precision  NOT NULL,
    Date        date NOT NULL,
    Time        time NOT NULL,
    Message     varchar(250) NOT NULL,
    ThreadId    integer references "Post"(PostID),
    Rating      integer NOT NULL,
    UserID      integer NOT NULL references "users"(user_id),
    UpdatedDate date NOT NULL,
    UpdatedTime time NOT NULL,
    ExpiredDate date NOT NULL
);
