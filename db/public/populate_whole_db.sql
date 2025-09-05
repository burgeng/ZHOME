.open preprocessing/data/housing.db 

-- create the table
create table if not exists "Regions_cleaned"
(
    regionid   integer not null
        constraint regions_cleaned_pk
            primary key,
    sizerank   integer,
    regionname text,
    regiontype text,
    statename  text,
    metro      text,
    countyname text,
    city       text,
    state      text
);

-- import the data
.mode csv
.import preprocessing/data/Regions_cleaned.csv Regions_cleaned

create table forsalelistings_processed_by_metro_cleaned
(
    regionid integer
        constraint forsalelistings_processed_by_metro_cleaned_regions_cleaned_regi
            references "Regions_cleaned",
    date     text,
    value    text
);

.import preprocessing/data/forSaleListings_processed_by-metro_cleaned.csv forsalelistings_processed_by_metro_cleaned

create table mhi_processed_by_metro_cleaned
(
    regionid integer
        constraint mhi_processed_by_metro_cleaned_regions_cleaned_regionid_fk
            references "Regions_cleaned",
    date     text,
    value    text
);

-- import the data
.import preprocessing/data/mhi_processed_by-metro_cleaned.csv mhi_processed_by_metro_cleaned

create table newconsales_processed_by_metro_cleaned
(
    regionid integer
        constraint newconsales_processed_by_metro_cleaned_regions_cleaned_regionid
            references "Regions_cleaned",
    date     text,
    value    text
);

-- import the data
.import preprocessing/data/newConSales_processed_by-metro_cleaned.csv newconsales_processed_by_metro_cleaned

create table zhvf_by_zhvf_metro_cleaned
(
    regionid integer
        constraint zhvf_by_zhvf_metro_cleaned_regions_cleaned_regionid_fk
            references "Regions_cleaned",
    basedate text,
    month    text,
    quarter  text,
    year     text
);

-- import the data
.import preprocessing/data/zhvf_by-zhvf_metro_cleaned.csv zhvf_by_zhvf_metro_cleaned

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

-- import the data
.import preprocessing/data/zhvf_by-zhvf_zip_cleaned.csv zhvf_by_zhvf_zip_cleaned

create table zhvi_processed_by_zhvi_city_cleaned
(
    regionid integer
        constraint zhvi_processed_by_zhvi_city_cleaned_regions_cleaned_regionid_fk
            references "Regions_cleaned",
    date     text,
    value    double precision
);

-- import the data
.import preprocessing/data/zhvi_processed_by-zhvi_city_cleaned.csv zhvi_processed_by_zhvi_city_cleaned

create table zhvi_processed_by_zhvi_county_cleaned
(
    regionid integer
        constraint zhvi_processed_by_zhvi_county_cleaned_regions_cleaned_regionid_
            references "Regions_cleaned",
    date     text,
    value    double precision
);

-- import the data
.import preprocessing/data/zhvi_processed_by-zhvi_county_cleaned.csv zhvi_processed_by_zhvi_county_cleaned

create table zhvi_processed_by_zhvi_metro_cleaned
(
    regionid integer
        constraint zhvi_processed_by_zhvi_metro_cleaned_regions_cleaned_regionid_f
            references "Regions_cleaned",
    date     text,
    value    double precision
);

-- import the data
.import preprocessing/data/zhvi_processed_by-zhvi_metro_cleaned.csv zhvi_processed_by_zhvi_metro_cleaned

create table zhvi_processed_by_zhvi_neighborhood_cleaned
(
    regionid integer
        constraint zhvi_processed_by_zhvi_neighborhood_cleaned_regions_cleaned_reg
            references "Regions_cleaned",
    date     text,
    value    text
);

-- import the data
.import preprocessing/data/zhvi_processed_by-zhvi_neighborhood_cleaned.csv zhvi_processed_by_zhvi_neighborhood_cleaned
create table zhvi_processed_by_zhvi_state_cleaned
(
    regionid integer
        constraint zhvi_processed_by_zhvi_state_cleaned_regions_cleaned_regionid_f
            references "Regions_cleaned",
    date     text,
    value    text
);

-- import the data
.import preprocessing/data/zhvi_processed_by-zhvi_state_cleaned.csv zhvi_processed_by_zhvi_state_cleaned

create table zhvi_processed_by_zhvi_zip_cleaned
(
    regionid integer
        constraint zhvi_processed_by_zhvi_zip_cleaned_regions_cleaned_regionid_fk
            references "Regions_cleaned",
    date     text,
    value    double precision
);

-- import the data
.import preprocessing/data/zhvi_processed_by-zhvi_zip_cleaned.csv zhvi_processed_by_zhvi_zip_cleaned

create table zori_processed_by_zori_city_cleaned
(
    regionid integer
        constraint zori_processed_by_zori_city_cleaned_regions_cleaned_regionid_fk
            references "Regions_cleaned",
    date     text,
    value    double precision
);

-- import the data
.import preprocessing/data/zori_processed_by-zori_city_cleaned.csv zori_processed_by_zori_city_cleaned

create table zori_processed_by_zori_county_cleaned
(
    regionid integer
        constraint zori_processed_by_zori_county_cleaned_regions_cleaned_regionid_
            references "Regions_cleaned",
    date     text,
    value    text
);

-- import the data
.import preprocessing/data/zori_processed_by-zori_county_cleaned.csv zori_processed_by_zori_county_cleaned

create table zori_processed_by_zori_metro_cleaned
(
    regionid integer
        constraint zori_processed_by_zori_metro_cleaned_regions_cleaned_regionid_f
            references "Regions_cleaned",
    date     text,
    value    text
);

-- import the data
.import preprocessing/data/zori_processed_by-zori_metro_cleaned.csv zori_processed_by_zori_metro_cleaned

create table zori_processed_by_zori_zip_cleaned
(
    regionid integer
        constraint zori_processed_by_zori_zip_cleaned_regions_cleaned_regionid_fk
            references "Regions_cleaned",
    date     text,
    value    double precision
);

-- import the data
.import preprocessing/data/zori_processed_by-zori_zip_cleaned.csv zori_processed_by_zori_zip_cleaned
