#!/usr/local/bin/python3
# coding: utf-8

from . import DOMAIN
from homeassistant.helpers.entity import Entity
from homeassistant.const import (ATTR_LATITUDE, ATTR_LONGITUDE)

ATTR_SPEED = 'speed'

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None) -> None:

    if discovery_info is None:
        return

    car_gps = hass.data[DOMAIN]["car_gps"]
    async_add_entities([CarGPSSensor(car_gps)])



class CarGPSSensor(Entity):

    def __init__(self, car_gps):
        self._name = 'Audi A4 GPS Tracker'
        self._icon = 'mdi:car'
        self._car_gps = car_gps
        self._unique_id = 'c5529293-6ec9-4ec0-bf71-065239fb8452'



    #for HASS
    @property
    def name(self):
        return self._name

    @property
    def state(self) -> str:
        return self._car_gps._last_upd

    @property
    def icon(self):
        return self._icon
    
    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self._unique_id

    @property
    def extra_state_attributes(self):
        attrs = {}
        attrs[ATTR_LATITUDE] = self._car_gps._lat
        attrs[ATTR_LONGITUDE] = self._car_gps._lon
        attrs[ATTR_SPEED] = self._car_gps._speed
        return attrs
