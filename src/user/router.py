from cities_light.models import Region, City
from django.core.paginator import Paginator
from ninja import Router, Query

from .schemas import Select2Response

router = Router()


@router.get("/get-region", response=Select2Response)
def list_region(
    request,
    country_id: str | int | None = Query(None),
    q: str = Query(None),
    page: int = 1,
):
    if not country_id or str(country_id).strip() in ["", "None", "null", "undefined"]:
        return {"results": [], "pagination": {"more": False}}

    try:
        country_id = int(country_id)
    except (ValueError, TypeError):
        return {"results": [], "pagination": {"more": False}}

    qs = Region.objects.filter(country_id=country_id)

    if q:
        qs = qs.filter(name__icontains=q)

    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)

    result = [{"id": item.id, "text": str(item)} for item in current_page.object_list]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/get-city", response=Select2Response)
def list_city(
    request,
    region_id: str | int | None = Query(None),
    q: str = Query(None),
    page: int = 1,
):
    if not region_id or str(region_id).strip() in ["", "None", "null", "undefined"]:
        return {"results": [], "pagination": {"more": False}}

    try:
        region_id = int(region_id)
    except (ValueError, TypeError):
        return {"results": [], "pagination": {"more": False}}

    qs = City.objects.filter(region_id=region_id)

    if q:
        qs = qs.filter(name__icontains=q)

    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)

    result = [{"id": item.id, "text": str(item)} for item in current_page.object_list]
    return {"results": result, "pagination": {"more": current_page.has_next()}}
