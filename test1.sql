create table user(
    id integer primary key,
    username character(8) unique not null,
    password character(16) not null
)

create table bandwidth(
    id integer primary key,
    time time  primary key not null,
    download character(100),
    upload character(100),
    ping character(100),
    isp character(100),
    foreign key (id) references user(id)
)

create table unusualflow(
    id integer primary key,
    time time  primary key not null,
    num_data integer not null,
    num_unusual integer,
    ip char(15) not null,
    port character(5) not null,
    foreign key (id) references user(id)
)