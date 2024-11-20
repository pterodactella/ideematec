from typing import Union
from pydantic import BaseModel, Field, field_validator


class Square(BaseModel):
    side: float = Field(..., gt=0, description="Side length must be greater than zero")

    @field_validator("side")
    def side_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Side value must be positive")
        return value


class Channel(BaseModel):
    height: float = Field(..., gt=0, description="Height must be greater than zero")
    width: float = Field(..., gt=0, description="Width must be greater than zero")

    @field_validator("height", "width")
    def dimensions_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Dimensions must be positive")
        return value


class DrawnShape(BaseModel):
    shape: Union[Square, Channel]
    thickness: float = Field(
        ..., gt=0, description="Thickness must be greater than zero"
    )

    @field_validator("thickness")
    def thickness_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Thickness value must be positive")
        return value

    def to_array(self):
        if isinstance(self.shape, Square):
            return ["Square", self.shape.side, self.shape.side, self.thickness]
        elif isinstance(self.shape, Channel):
            return ["Channel", self.shape.height, self.shape.width, self.thickness]
