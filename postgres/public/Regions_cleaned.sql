create table "Regions_cleaned"
(
    regionid   integer not null
        constraint regions_cleaned_pk
            primary key,
    sizerank   integer,
    regionname text,
    regiontype text,
    statename  text,
    metro      text,
    countyname text,
    city       text,
    state      text
);

alter table "Regions_cleaned"
    owner to postgres;

