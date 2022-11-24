import csv
from dataclasses import dataclass, field
from typing import List

from src.trade import TradeStat
from src.trade.config import *

COUNTRY_FILE = "data/trade_data/countries.csv"


@dataclass
class Country:
  iso: str
  lat: float
  long: float
  name: str


@dataclass
class UnifiedStats:
  indicators: List[TradeStat] = field(default_factory=list)
  countries: List[Country] = field(default_factory=list)
  region_list: List[TradeStat] = field(default_factory=list)

  def filter(self):
    with open(COUNTRY_FILE, "r") as out:
      data = csv.reader(out)
      next(data)  # skip header
      for row in data:
        self.countries.append(
          Country(row[0].strip(), row[1].strip(), row[2].strip(),
                  row[3].strip("\"| ")))
    # filter
    self.clean()

  def get_long(self) -> List[float]:
    return [i.country_info.long for i in self.indicators]

  def get_lat(self) -> List[float]:
    return [i.country_info.lat for i in self.indicators]

  def get_country_names(self, geospatial=True) -> List[str]:
    if geospatial:
      return [i.country_info.name for i in self.indicators]
    else:
      return [i.partner for i in self.indicators]

  def get_max(self, year) -> float:
    max = 0
    for i in self.indicators:
      data = i.stats.get(year)
      if data:
        if float(data) > max:
          max = float(i.stats.get(year))
    return max

  def product_codes(self) -> List[str]:
    unique = set()
    for i in self.indicators:
      unique.add(i.productcode)
    return list(unique)

  def extend(self, gindicator: List[TradeStat]) -> None:
    '''
        add list of GI objects to BaseStats
        '''
    self.indicators.extend(gindicator)

  def get_indicator(self,
                    reporter: str = "Singapore",
                    partner: str = None,
                    indicator: str = None,
                    productcode: str = None) -> List[TradeStat]:
    '''
        iterate all GI objects and get the match based on
        partner, indicator, reporter and product code

        example:
        BaseStats.get_indicator(indicator="Exports", reporter="Singapore",
                                partner="World", productcode="Fuels")
        '''
    params = {
      'reporter': reporter,
      'partner': partner,
      'indicator': indicator,
      'productcode': productcode
    }
    filtered = {k: v for k, v in params.items() if v is not None}
    params.clear()
    params.update(filtered)
    comp = list(i for i in self.indicators if i == params)
    return comp

  def clean(self) -> None:
    """Filters indicators with partners listed in
        TO_REMOVE and
        update country names in NAME_CHANGE
        """
    to_keep = []
    region_list = []
    for i in self.indicators:
      if i.partner not in TO_REMOVE:
        if i.partner in REGIONS:
          region_list.append(i)
          continue
        if i.partner in NAME_CHANGE:
          new_partner = NAME_CHANGE[i.partner]
          i.partner = new_partner
        c_list = []
        for c in self.countries:
          if c.name == i.partner:
            c_list.append(c)
        i.country_info = [c for c in self.countries if c.name == i.partner][0]
        to_keep.append(i)
    self.indicators = to_keep
    self.region_list = region_list

  def print(self) -> None:
    for i in self.indicators:
      print(i)
