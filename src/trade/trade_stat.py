from dataclasses import dataclass, field
from typing import DefaultDict, Dict


@dataclass
class TradeStat:
  reporter: str
  partner: str
  indicator: str
  productcode: str
  country_info: str
  stats: Dict[int, float] = field(default_factory=lambda: DefaultDict(dict))

  def add(self, year: int, data: float) -> None:
    '''
        add data into the year as value
        '''
    self.stats[year] = data

  def __eq__(self, kwargs) -> bool:
    '''
        compare all indicators to return GI object
        '''
    for arg in kwargs:
      comp = getattr(self, arg)
      if comp != kwargs[arg]:
        return False
    return True

  def __repr__(self) -> str:
    return f"Partner: {str(self.partner)}, PC: {str(self.productcode)}, Indicator: {str(self.indicator)}."

  def to_dict(self):
    """
        converts to dict for pandas df
        """
    return {
      'reporter': self.reporter,
      'partner': self.partner,
      'indicator': self.indicator,
      'productcode': self.productcode,
      'years': self.stats.keys(),
      'data': self.stats.values()
    }
