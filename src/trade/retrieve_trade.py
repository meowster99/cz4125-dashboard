import csv
import logging
import os
from dataclasses import dataclass, field
from typing import List

from src.trade import TradeStat


@dataclass
class Retrieve:
  folder: str
  years: List = field(default_factory=lambda: [i for i in range(1989, 2021)])
  stats: List = field(default_factory=list)

  def __post_init__(self):
    '''
        checks whether dir exists
        '''
    if not os.path.exists(self.folder):
      logging.error("Folder does not exist!")

  def retrieve(self):
    '''
        iterates all files in dir and get stats as GI obj
        and adds them to BaseStat obj
        '''
    for dat_file in os.listdir(self.folder):
      try:
        stat = create_stat(f"{self.folder}/{dat_file}", self.years)
        self.stats.extend(stat)
      except Exception as e:
        logging.error(f"{dat_file} in {self.folder} cannot"
                      f" be read. Due to {e.args}")


def create_stat(file_name: str, years_list: List[int]) -> List[TradeStat]:
  '''
    creates GI objs from rows in csv file
    '''
  bs = []
  with open(file_name, "r") as out:
    data = csv.reader(out)
    next(data)  # skip header
    for row in data:
      trade_data = []
      for i in row[:4:-1]:
        if i:
          trade_data.append(float(i))
        else:
          trade_data.append(float(0))
      trade_data.reverse()
      bs.append(
        TradeStat(reporter=row[0].strip("\"| "),
                  partner=row[1].strip("\"| "),
                  indicator=row[2].strip("\"| "),
                  productcode=row[3].strip("\"| "),
                  country_info=None,
                  stats=dict(zip(years_list, trade_data))))
  return bs
