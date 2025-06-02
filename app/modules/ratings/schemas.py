from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class RatingEnum(Enum):
    rating_0_5 = 0.5
    rating_0_0 = 0.0
    rating_1_0 = 1.0
    rating_1_5 = 1.5
    rating_2_0 = 2.0
    rating_2_5 = 2.5
    rating_3_0 = 3.0
    rating_3_5 = 3.5
    rating_4_0 = 4.0
    rating_4_5 = 4.5
    rating_5_0 = 5.0

class RatingBase(BaseModel):
    value: Optional[RatingEnum] = Field(default=RatingEnum.rating_4_0)