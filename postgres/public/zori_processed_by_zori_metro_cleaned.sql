create table zori_processed_by_zori_metro_cleaned
(
    regionid integer
        constraint zori_processed_by_zori_metro_cleaned_regions_cleaned_regionid_f
            references "Regions_cleaned",
    date     text,
    value    text
);

alter table zori_processed_by_zori_metro_cleaned
    owner to postgres;

