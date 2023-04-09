from Loggers import *
from CellObjects import TimeCell

logger = TimeLogger()
logger.clear()
logger.add(cell=TimeCell(action="мамачка"))
print(OracleLogger().get())
