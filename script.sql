create table userinfo
(
    id        int         not null
        primary key,
    mobile    varchar(11) not null,
    password  varchar(64) not null,
    real_name varchar(16) not null,
    role      tinyint     not null
);

insert into userinfo(id, mobile, password, real_name, role)
VALUES (1, '15231700000', 'root', 'root', 2);

create table `order`
(
    id      int auto_increment
        primary key,
    url     varchar(255) not null,
    count   int          not null,
    user_id int          not null,
    status  tinyint      null,
    constraint fk_user_order
        foreign key (user_id) references userinfo (id)
);


