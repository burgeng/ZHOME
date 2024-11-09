create table forsalelistings_processed_by_metro_cleaned
(
    regionid integer
        constraint forsalelistings_processed_by_metro_cleaned_regions_cleaned_regi
            references "Regions_cleaned",
    date     text,
    value    text
);

alter table forsalelistings_processed_by_metro_cleaned
    owner to postgres;

