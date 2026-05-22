class DataMapper:
    schema = None
    model = None

    @classmethod
    def alchemy_to_pydantic(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def pydantic_to_alchemy(cls, data):
        return cls.model(**data.model_dump())
