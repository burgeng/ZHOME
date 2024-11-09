create table zhvi_processed_by_zhvi_state_cleaned
(
    regionid integer
        constraint zhvi_processed_by_zhvi_state_cleaned_regions_cleaned_regionid_f
            references "Regions_cleaned",
    date     text,
    value    text
);

alter table zhvi_processed_by_zhvi_state_cleaned
    owner to postgres;

