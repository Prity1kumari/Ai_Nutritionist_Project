from pydantic import BaseModel, Field


class FoodInput(BaseModel):

    energy: float = Field(
        ...,
        ge=0,
        description="Energy (kcal per 100g)",
        example=250
    )

    fat: float = Field(
        ...,
        ge=0,
        description="Fat (g per 100g)",
        example=12.5
    )

    saturated_fat: float = Field(
        ...,
        ge=0,
        description="Saturated Fat (g per 100g)",
        example=4.5
    )

    carbs: float = Field(
        ...,
        ge=0,
        description="Carbohydrates (g per 100g)",
        example=35
    )

    sugar: float = Field(
        ...,
        ge=0,
        description="Sugar (g per 100g)",
        example=15
    )

    fiber: float = Field(
        ...,
        ge=0,
        description="Fiber (g per 100g)",
        example=6
    )

    protein: float = Field(
        ...,
        ge=0,
        description="Protein (g per 100g)",
        example=8
    )

    salt: float = Field(
        ...,
        ge=0,
        description="Salt (g per 100g)",
        example=0.8
    )

    ingredients: str = Field(
        ...,
        description="Comma separated ingredient list",
        example="Sugar, Palm Oil, Sodium Nitrate"
    )