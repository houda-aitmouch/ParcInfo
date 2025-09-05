import os
import time


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ParcInfo.settings")
    try:
        import django  # type: ignore
        django.setup()
    except Exception as exc:  # pragma: no cover
        print(f"[chatbot] Django setup error: {exc}")
        raise

    try:
        # Import the core chatbot after Django is ready
        import apps.chatbot.core_chatbot as core  # type: ignore
    except Exception as exc:  # pragma: no cover
        print(f"[chatbot] Failed to import core_chatbot: {exc}")
        raise

    # If the module exposes a main() function, call it. Otherwise, rely on module side-effects
    try:
        if hasattr(core, "main") and callable(getattr(core, "main")):
            core.main()
        else:
            # Keep process alive if import doesn't block
            while True:
                time.sleep(60)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()


