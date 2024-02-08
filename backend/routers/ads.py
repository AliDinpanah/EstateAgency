from typing import Annotated
from pydantic import BaseModel, Field, validator

import json
import datetime
from loguru import logger
import random
import httpx
from fastapi import APIRouter, Security, HTTPException, status, Body, Response, Depends
from auth import check_token
import db
import auth
import yaml

config = yaml.safe_load(open("./data/config.yaml"))

router = APIRouter(prefix="/ads")


class AdInput(BaseModel):
    city: str = Field(..., min_length=2, max_length=100)
    district: str = Field(..., min_length=2, max_length=100)
    title: str | None = Field(None, min_length=2, max_length=255)
    description: str | None = Field(None, min_length=2)
    rooms_count: int = Field(..., ge=1, le=10)
    price: float | None = Field(None, ge=0)
    rent: float | None = Field(None, ge=0)
    mortgage: float | None = Field(None, ge=0)
    metrage: float = Field(..., ge=0)
    property_type: str = Field(..., max_length=15)
    facilities: list = Field(..., min_items=0)
    conditions: list = Field(..., min_items=0)
    images: list = Field(..., min_items=1)
    primary_image: str = Field(..., min_length=2, max_length=255)

    @validator("property_type")
    def application_upper(cls, v):
        if v.lower() not in ["residential", "commercial", "office", "industrial"]:
            raise ValueError("Invalid application type")
        return v.lower()


class SearchInput(BaseModel):
    text: str | None = Field(None, min_length=0)
    min_price: float | None = Field(None, ge=-1)
    max_price: float | None = Field(None, ge=-1)
    min_rent: float | None = Field(None, ge=-1)
    max_rent: float | None = Field(None, ge=-1)
    min_mortgage: float | None = Field(None, ge=-1)
    max_mortgage: float | None = Field(None, ge=-1)
    min_rooms_count: int | None = Field(None, ge=0)
    max_rooms_count: int | None = Field(None, ge=0)
    ad_type: str | None = Field(None)
    property_type: str | None = Field(None)
    facilities: list[int] | None = Field(None)
    conditions: list[int] | None = Field(None)
    agency_id: int | None = Field(None)


def price_to_str(price):
    if price == -1:
        return "Negotiable"
    elif price:
        return f"{price} $"
    return None


@router.get("/facilities/")
async def get_facilities():
    query = "SELECT id, name FROM facilities"
    facilities = db.fetch_all(query)
    return [{"id": facility[0], "name": facility[1]} for facility in facilities]

@router.get("/conditions/")
async def get_conditions():
    query = "SELECT id, name FROM conditions"
    conditions = db.fetch_all(query)
    return [{"id": condition[0], "name": condition[1]} for condition in conditions]

@router.post("/add/")
async def add_ad(ad: AdInput, response: Response, user_info: dict = Depends(check_token)):
    if not user_info['role'] == 'agency':
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"status": "failed", "message": "Only agencies can add ads"}
    
    query = """
    INSERT INTO ads (city, district, title, description, rooms_count, price, rent, mortgage, metrage, property_type, primary_image, uid, agency_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, (SELECT id FROM agencies WHERE admin_phone = %s))
    """
    uid = random.randint(1000000, 9999999)
    values = (ad.city, ad.district, ad.title, ad.description, ad.rooms_count, ad.price, ad.rent, ad.mortgage, ad.metrage, ad.property_type, ad.primary_image, uid, user_info['phone'])
    cursor = db.execute_query(query, values)
    ad_id = cursor.lastrowid
    if ad_id:
        query = """
        INSERT INTO ads_facilities (ad_id, facility_id)
        VALUES (%s, %s)
        """
        values = [(ad_id, facility_id) for facility_id in ad.facilities]
        db.executemany(query, values)
        query = """
        INSERT INTO ads_conditions (ad_id, condition_id)
        VALUES (%s, %s)
        """
        values = [(ad_id, condition_id) for condition_id in ad.conditions]
        db.executemany(query, values)
        query = """
        INSERT INTO ads_images (ad_id, image_filename)
        VALUES (%s, %s)
        """
        values = [(ad_id, image_filename) for image_filename in ad.images]
        db.executemany(query, values)
        response.status_code = status.HTTP_201_CREATED
        return {"id": ad_id}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add ad")
    

@router.get("/get/{ad_uid}")
async def get_ad(ad_uid: int, response: Response):
    query = """
    SELECT ads.id, ads.city, district, title, description, rooms_count, price, rent, mortgage, metrage, property_type, primary_image, agencies.name, agencies.phone, agencies.id
    FROM ads
    JOIN agencies ON agencies.id = ads.agency_id
    WHERE uid = %s
    """
    result = db.fetch_one(query, (ad_uid,))
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "failed", "message": "Ad not found"}
    ad = {
        "id": result[0],
        # use a default title based on the property type, ad_type and city if title is not provided
        "title": result[3] if result[3] else f"{result[10]} in {result[1]} for {'sale' if result[6] else 'rent'}",
        "description": result[4],
        "ad_type": "sale" if result[6] else "rent",
        "primary_image": "http://127.0.0.1:8000/files/" + result[11],
        "agency_id": result[14],
        "details": {
            "Agency": result[12],
            "Agency phone": result[13],
            "City": result[1],
            "District": result[2],
            "Number of rooms": result[5],
            "Metrage": "{} m²".format(result[9]),
            "Property type": result[10]
        }
    }

    if ad["ad_type"] == "sale":
        ad["details"]["Price"] = price_to_str(result[6])
    else:
        ad["details"]["Rent"] = price_to_str(result[7])
        ad["details"]["Mortgage"] = price_to_str(result[8])
    
    query = """
    SELECT facilities.id, facilities.name
    FROM facilities
    JOIN ads_facilities ON facilities.id = ads_facilities.facility_id
    WHERE ads_facilities.ad_id = %s
    """
    facilities = db.fetch_all(query, (ad['id'],))
    ad['facilities'] = [{"id": facility[0], "name": facility[1]} for facility in facilities]
    query = """
    SELECT conditions.id, conditions.name
    FROM conditions
    JOIN ads_conditions ON conditions.id = ads_conditions.condition_id
    WHERE ads_conditions.ad_id = %s
    """
    conditions = db.fetch_all(query, (ad['id'],))
    ad['conditions'] = [{"id": condition[0], "name": condition[1]} for condition in conditions]
    query = """
    SELECT image_filename
    FROM ads_images
    WHERE ad_id = %s
    """
    images = db.fetch_all(query, (ad['id'],))
    images = [result[11]] + [image[0] for image in images if image[0] != result[11]]
    ad['images'] = [f"http://127.0.0.1:8000/files/{image}" for image in images]
    return ad

@router.post("/search/")
async def search_ads(response: Response, search: SearchInput = Body(...)):
    query = "SELECT uid, title, description, city, district, price, rent, mortgage, primary_image FROM ads WHERE "
    values = []
    conditions = []

    if search.text:
        words = search.text.split()
        word_conditions = []
        for word in words:
            word_condition = "(title LIKE %s OR description LIKE %s OR city LIKE %s OR district LIKE %s)"
            word_conditions.append(word_condition)
            values.extend(["%" + word + "%"] * 4)
        combined_word_conditions = " AND ".join(word_conditions)
        conditions.append(f"({combined_word_conditions})")

    if search.min_price is not None:
        conditions.append("price >= %s")
        values.append(search.min_price)

    if search.max_price is not None:
        conditions.append("price <= %s")
        values.append(search.max_price)

    if search.min_rent is not None:
        conditions.append("rent >= %s")
        values.append(search.min_rent)

    if search.max_rent is not None:
        conditions.append("rent <= %s")
        values.append(search.max_rent)

    if search.min_mortgage is not None:
        conditions.append("mortgage >= %s")
        values.append(search.min_mortgage)

    if search.max_mortgage is not None:
        conditions.append("mortgage <= %s")
        values.append(search.max_mortgage)

    if search.min_rooms_count is not None:
        conditions.append("rooms_count >= %s")
        values.append(search.min_rooms_count)

    if search.max_rooms_count is not None:
        conditions.append("rooms_count <= %s")
        values.append(search.max_rooms_count)
    
    if search.ad_type:
        conditions.append("price IS NOT NULL" if search.ad_type == "sale" else "price IS NULL")
    
    if search.property_type and search.property_type != "all":
        conditions.append("property_type = %s")
        values.append(search.property_type)


    if search.facilities:
        facilities_placeholders = ', '.join(['%s'] * len(search.facilities))
        facilities_subquery = f"id IN (SELECT ad_id FROM ads_facilities WHERE facility_id IN ({facilities_placeholders}) GROUP BY ad_id HAVING COUNT(DISTINCT facility_id) = %s)"
        conditions.append(facilities_subquery)
        values.extend(search.facilities)
        values.append(len(search.facilities))

    if search.conditions:
        conditions_placeholders = ', '.join(['%s'] * len(search.conditions))
        conditions_subquery = f"id IN (SELECT ad_id FROM ads_conditions WHERE condition_id IN ({conditions_placeholders}) GROUP BY ad_id HAVING COUNT(DISTINCT condition_id) = %s)"
        conditions.append(conditions_subquery)
        values.extend(search.conditions)
        values.append(len(search.conditions))
    
    if search.agency_id:
        conditions.append("agency_id = %s")
        values.append(search.agency_id)
    
    query += " AND ".join(conditions)

    if query.endswith("WHERE "):
        query = query[:-6]

    query += " ORDER BY id DESC LIMIT 12"

    print(query)
    print(values)

    results = db.fetch_all(query, tuple(values))
    if not results:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "failed", "message": "No ads found matching criteria"}

    results_dicts = []
    for result in results:
        ad = {
            "id": result[0],
            "title": result[1],
            "description": result[2],
            "city": result[3],
            "district": result[4],
            "price": price_to_str(result[5]),
            "rent": price_to_str(result[6]),
            "mortgage": price_to_str(result[7]),
            "primary_image": "http://127.0.0.1:8000/files/" + result[8]
        }
        results_dicts.append(ad)
    return results_dicts
