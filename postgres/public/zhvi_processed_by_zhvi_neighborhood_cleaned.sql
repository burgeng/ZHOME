create table zhvi_processed_by_zhvi_neighborhood_cleaned
(
    regionid integer
        constraint zhvi_processed_by_zhvi_neighborhood_cleaned_regions_cleaned_reg
            references "Regions_cleaned",
    date     text,
    value    text
);

alter table zhvi_processed_by_zhvi_neighborhood_cleaned
    owner to postgres;

