from edc_map.mappers import BaseAreaMapper
from edc_map.classes import site_mappers

from ..models import RecentInfection


class MochudiMapper(BaseAreaMapper):

    item_model = RecentInfection
    map_area = 'mochudi'
    map_code = '10'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = 24.124
    gps_center_lon = 22.343
    radius = 5.5
    location_boundary = ()

site_mappers.register(MochudiMapper)
