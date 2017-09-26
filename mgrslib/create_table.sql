drop table if exists m6_geo.ENTITY_HASH;
create table m6_geo.ENTITY_FILTER(
 ID BIGINT AUTO_INCREMENT PRIMARY KEY,
 ENTITY_ID INTEGER NOT NULL,
 ENTITY_TYPE SMALLINT NOT NULL,
 SPACE SMALLINT NOT NULL,
 KEY_COUNT INTEGER,
 HASH LONGBLOB COMMENT "Pickle of this bloomfilter",
 HIT_DATE INTEGER NOT NULL,
 CREATED_AT TIMESTAMP NOT NULL DEFAULT NOW(),
 INDEX ENTITY_FILTER_ENTITY(ENTITY_ID, ENTITY_TYPE),
 INDEX ENTITY_FILTER_TIME(HIT_DATE),
 INDEX ENTITY_FILTER_ENTITY_TYPE(ENTITY_TYPE),
 INDEX ENTITY_FILTER_SPACE(SPACE)
);

drop table pl.FILTER_ENTITIES;
create table pl.FILTER_ENTITIES(
bestdeviceid string,
entity int
)
 PARTITIONED BY(entity_type int,space int, hit_date int) sort by (entity)
row format delimited fields terminated by '\t' stored as textfile;


set hive.exec.dynamic.partition=true;  
set hive.exec.dynamic.partition.mode=nonstrict; 

insert overwrite table pl.FILTER_ENTITIES partition(entity_type,space,hit_date)
select
nuid bestdeviceid,
entity,
entity_id_type_parent entity_type,
space,
20170828 hit_date
from
pl.AVAILS_ENTITIES;





select * from pl.AVAILS_ENTITIES 