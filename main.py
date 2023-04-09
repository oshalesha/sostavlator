from Loggers import TimeLogger
from CellObjects import TimeCell

logger = TimeLogger()

logger.add_time_cell(TimeCell(action="Диффуры"))
logger.add_time_cell(TimeCell(action="уборка спальни"))
logger.add_time_cell(TimeCell(action="уборка комнат"))
logger.add_time_cell(TimeCell(action="обед"))
