drop table if exists shortlinks;
create table shortlinks (
  id integer primary key autoincrement,
  link_id text not null,
  link_url text not null,
  link_hits integer not null
);