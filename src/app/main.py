from .api import router
from .core.config import settings
from .core.setup import create_application
from .core.trace_manager import trace_manager_inst


if settings.IS_DEBUG_ENABLED:
    import debugpy

    debugpy.listen(("0.0.0.0", 5678))
    print("⏳ Waiting for debugger to attach...")
    # debugpy.wait_for_client()
    # print("🎉 Debugger attached!")

trace_manager_inst.enable()
app = create_application(router=router, settings=settings)