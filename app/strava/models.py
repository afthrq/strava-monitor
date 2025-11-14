from dataclasses import dataclass

@dataclass
class Activity:
    id: int
    name: str
    type: str
    distance: float
    moving_time: int
    start_date: str
