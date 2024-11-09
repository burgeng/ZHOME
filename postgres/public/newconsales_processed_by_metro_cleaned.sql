create table newconsales_processed_by_metro_cleaned
(
    regionid integer
        constraint newconsales_processed_by_metro_cleaned_regions_cleaned_regionid
            references "Regions_cleaned",
    date     text,
    value    text
);

alter table newconsales_processed_by_metro_cleaned
    owner to postgres;

