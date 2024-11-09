create table zori_processed_by_zori_county_cleaned
(
    regionid integer
        constraint zori_processed_by_zori_county_cleaned_regions_cleaned_regionid_
            references "Regions_cleaned",
    date     text,
    value    text
);

alter table zori_processed_by_zori_county_cleaned
    owner to postgres;

