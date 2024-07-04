from typing import List

from pydantic import BaseModel


class GetCategoriesResponse(BaseModel):
    class Category(BaseModel):
        display: str
        slug: str

    categories: List[Category] = None


class GetCitiesResponse(BaseModel):
    class City(BaseModel):
        display: str
        slug: str

    cities: List[City] = None


class GetDistrictsResponse(BaseModel):
    class District(BaseModel):
        display: str
        slug: str

    districts: List[District] = None


class GetBrandModelsResponse(BaseModel):
    class BrandModel(BaseModel):
        display: str
        slug: str

    brand_models: List[BrandModel] = None


class GetColorsResponse(BaseModel):
    class Color(BaseModel):
        display: str
        slug: str

    colors: List[Color] = None


class GetMobileInternalStoragesResponse(BaseModel):
    class InternalStorage(BaseModel):
        display: str
        slug: str

    internal_storages: List[InternalStorage] = None


class GetMobileRamMemoriesResponse(BaseModel):
    class InternalStorage(BaseModel):
        display: str
        slug: str

    ram_memories: List[InternalStorage] = None


class GetLightBodyStatusResponse(BaseModel):
    class BodyStatus(BaseModel):
        display: str
        slug: str

    body_status: List[BodyStatus] = None
