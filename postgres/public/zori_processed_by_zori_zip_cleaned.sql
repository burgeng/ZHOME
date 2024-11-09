create table zori_processed_by_zori_zip_cleaned
(
    regionid integer
        constraint zori_processed_by_zori_zip_cleaned_regions_cleaned_regionid_fk
            references "Regions_cleaned",
    date     text,
    value    double precision
);

alter table zori_processed_by_zori_zip_cleaned
    owner to postgres;

