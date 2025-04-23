from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from typing import List


class InputField(BaseModel):
    id: str = Field(description="id that helps in uniquely identifying the input field using selenium")
    id_type: str = Field(description="type of id to be used in selenium to identify the input field")
    desc: str = Field(description="description about the input field. The data it expects")


class Form(BaseModel):
    fields: List[InputField] = Field(description="all fields in the form")



form_parser = PydanticOutputParser(pydantic_object = Form)
