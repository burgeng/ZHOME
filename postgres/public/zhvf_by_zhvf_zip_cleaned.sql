create table zhvf_by_zhvf_zip_cleaned
(
    regionid integer
        constraint zhvf_by_zhvf_zip_cleaned_regions_cleaned_regionid_fk
            references "Regions_cleaned",
    basedate text,
    month    text,
    quarter  text,
    year     text
);

alter table zhvf_by_zhvf_zip_cleaned
    owner to postgres;

