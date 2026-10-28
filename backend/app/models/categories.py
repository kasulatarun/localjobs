from pydantic import BaseModel, Field

class Category(BaseModel):
    category_id: str = Field(..., alias="CategoryID")
    name: str = Field(..., alias="Name")
    telugu_name: str = Field(..., alias="TeluguName")
    hindi_name: str = Field(..., alias="HindiName")
    english_name: str = Field(..., alias="EnglishName")
    active: bool = Field(True, alias="Active")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }
