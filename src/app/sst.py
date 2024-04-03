from mangum import Mangum

from app.core.application import get_application

app = get_application()
handler = Mangum(app, lifespan="off")
