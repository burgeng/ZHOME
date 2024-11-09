create table sales_processed_by_metro_cleaned
(
    regionid integer
        constraint sales_processed_by_metro_cleaned_regions_cleaned_regionid_fk
            references "Regions_cleaned",
    date     text,
    value    text
);

alter table sales_processed_by_metro_cleaned
    owner to postgres;

