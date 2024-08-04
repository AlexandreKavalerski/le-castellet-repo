from .api import router
from .core.config import settings
from .core.setup import create_application


if settings.IS_DEBUG_ENABLED:
    import debugpy

    debugpy.listen(("0.0.0.0", 5678))
    print("⏳ Waiting for debugger to attach...")
    # debugpy.wait_for_client()
    # print("🎉 Debugger attached!")

app = create_application(router=router, settings=settings)
