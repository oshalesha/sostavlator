from Loggers import TimeLogger
from Oracle import TimeOracle
from CellObjects import TimeCell

oracle = TimeOracle()
logger = TimeLogger()
logger.add(TimeCell(action="поездка в израиль"))
print(oracle.predict())
