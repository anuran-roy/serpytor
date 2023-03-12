import uvicorn
from aiohttp import web

app = web.Application()
router = web.RouteTableDef()


@router.get("/dashboard")
async def get_pipeline_data(request) -> None:
    pass


app.add_routes(routes=router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000, log_level="info")
