[![Test-Lint-Format](https://github.com/aurelpere/python-planif/actions/workflows/main.yml/badge.svg)](https://github.com/aurelpere/python-planif/actions/workflows/main.yml) ![test-coverage badge](./coverage-badge.svg) [![Maintainability](https://api.codeclimate.com/v1/badges/737c2dcaa384fb64bbbe/maintainability)](https://codeclimate.com/github/aurelpere/python-planif/maintainability)

# planif

This is two python scripts using openstreertmap data and ocsge data


## process osm and ocsge data
<br>

`osm2pgsql -d gis -C 53 --create --drop midi-pyrenees-latest.osm.pbf -p osm -E 27572 --slim`<br>
>create a gis database with osm data (midi-pyrenees)
<br>


`create table hautegaronne as (SELECT * FROM osm_polygon WHERE name = 'Haute-Garonne')`<br>
>create a table of haute garonne department
<br>


`ogr2ogr -nlt POLYGON -append -t_srs "EPSG:27572" -f PostgreSQL PG:"dbname=gis host=localhost user=user password=pw" OCS_GE_1-1_2013_SHP_LAMB93_D031_2018-03-12/OCS_GE/1_DONNEES_LIVRAISON_2018-03-00296/OCSGE_1-1_SHP_LAMB93_D31-2013/OCCUPATION_SOL.shp`<br>
>add ocsge data of haute-garonne to gis database
<br>


`SELECT osm.*, h.* FROM osm_fuel osm JOIN hautegaronne h ON ST_contains(h.way, ST_GeometryFromText(osm.geometry,27572));`<br>
>select fuel stations in hautegaronne
<br>


`SELECT osm.*, h.* FROM osm_polygon osm JOIN hautegaronne h ON ST_contains(h.way, ST_GeometryFromText(osm.geometry,27572));`<br>
>select buildings in hautegaronne
<br>


`psql -A --command "SELECT osm_id, name, building as type, st_astext(way) as geometry FROM osm_polygon WHERE building IS NOT NULL" --dbname gis --username user --output building.csv --field-separator '#'`<br>
>extract building.csv from gis database
<br>


`psql -A --command "SELECT ogc_fid,id,code_cs,millesime,source, st_astext(wkb_geometry) as geometry FROM occupation_sol WHERE code_cs in ('CS2.2.1')" --dbname gis --username user --output occsol.csv --field-separator '#'`<br>
>extract occsol.csv from gis database
<br>


`psql -A --command "SELECT osm_id, name, amenity  as type, st_astext(way) as geometry FROM osm_point WHERE amenity in ('fuel','charging_station') UNION ALL SELECT osm_id, name, amenity  as type, st_astext(way) as geometry FROM osm_polygon WHERE amenity in ('fuel','charging_station') UNION ALL SELECT osm_id, name, shop  as type,st_astext(way) as geometry FROM osm_point WHERE shop in ('fuel') UNION ALL SELECT osm_id, name, shop as type, st_astext(way) as geometry FROM osm_polygon WHERE shop in ('fuel')" --dbname gis --username user --output carfuel.csv --field-separator '#'`<br>
>extract carfuel.csv from gis database
<br>


## python usage

`python geotherm.py -b building.csv -o occsol.csv`<br>
>process building.csv to append a column 'geot' set to yes if the building can accept a geothermal installation (has a garden)
<br>


`python stations.py -s stations.csv -o occsol.csv`<br>
>process stations.csv to append a column 'p2g' set to yes if the fuel station can accept a power to gas installation (has 12ha of land available at a 1 km distance)
<br>

## results
building accepting geothermy:
![geotherm](./buildings_geot.png)

carfuel stations accepting power to gas
![stations](./stations_p2g.png)
