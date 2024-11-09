create table zhvi_processed_by_zhvi_county_cleaned
(
    regionid integer
        constraint zhvi_processed_by_zhvi_county_cleaned_regions_cleaned_regionid_
            references "Regions_cleaned",
    date     text,
    value    double precision
);

alter table zhvi_processed_by_zhvi_county_cleaned
    owner to postgres;

