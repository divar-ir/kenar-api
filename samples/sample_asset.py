from samples.sample_app import app

if __name__ == "__main__":
    resp = app.asset.get_categories()
    print(resp.categories)

    resp = app.asset.get_cities()
    print(resp.cities)

    resp = app.asset.get_districts()
    print(resp.districts)

    resp = app.asset.get_city_districts(city="tehran")
    print(resp.districts)

    resp = app.asset.get_brand_models(category="light")
    print(resp.brand_models)

    resp = app.asset.get_colors(category="mobile-phones")
    print(resp.colors)

    resp = app.asset.get_mobile_internal_storages()
    print(resp.internal_storages)

    resp = app.asset.get_mobile_ram_memories()
    print(resp.ram_memories)

    resp = app.asset.get_light_body_status()
    print(resp.body_status)
