create table categories
(
    id          int          not null
        primary key,
    name        varchar(45)  not null,
    description varchar(64)  null,
    icon_link   varchar(256) null
)
    charset = utf8mb3;

create table regions
(
    id   int         not null
        primary key,
    name varchar(64) not null
)
    charset = utf8mb3;

create table users
(
    id         int auto_increment
        primary key,
    name       varchar(45)          not null,
    surname    varchar(45)          not null,
    username   varchar(45)          not null,
    email      varchar(64)          not null,
    has_avatar tinyint(1) default 0 not null,
    region     int                  not null,
    birthdate  date                 not null,
    disabled   tinyint(1) default 0 not null,
    constraint username_UNIQUE
        unique (username),
    constraint user_fk_region
        foreign key (region) references regions (id)
)
    charset = utf8mb3;

create table events
(
    id            int auto_increment
        primary key,
    title         varchar(45)   not null,
    address       varchar(128)  not null,
    region        int           not null,
    description   varchar(256)  not null,
    price         int default 0 not null,
    max_people    int default 0 not null,
    category      int default 0 null,
    is_online     tinyint(1)    not null,
    start_date    datetime      not null,
    end_date      datetime      not null,
    icon          int           null,
    author        int           not null,
    creation_date datetime      not null,
    constraint event_fk_region
        foreign key (region) references regions (id),
    constraint events_fk_category
        foreign key (category) references categories (id)
            on update cascade on delete set null,
    constraint fk_author
        foreign key (author) references users (id)
            on update cascade on delete cascade
)
    charset = utf8mb3;

create index fk_author_idx
    on events (author);

create table user_event
(
    user   int                           not null,
    event  int                           not null,
    status enum ('accepted', 'rejected') not null,
    primary key (user, event),
    constraint fk_user
        foreign key (user) references users (id)
            on update cascade on delete cascade,
    constraint user_event_fk_event
        foreign key (event) references events (id)
)
    charset = utf8mb3;

create index fk_event_idx
    on user_event (event);


