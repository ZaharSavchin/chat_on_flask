drop table if exists entries;
create table entries (
    id INTEGER primary key autoincrement,
    title text not null,
    text text not null
);