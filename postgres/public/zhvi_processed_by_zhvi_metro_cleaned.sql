create table zhvi_processed_by_zhvi_metro_cleaned
(
    regionid integer
        constraint zhvi_processed_by_zhvi_metro_cleaned_regions_cleaned_regionid_f
            references "Regions_cleaned",
    date     text,
    value    double precision
);

alter table zhvi_processed_by_zhvi_metro_cleaned
    owner to postgres;

