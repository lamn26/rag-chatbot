from app.api.dependencies import get_chat_service

def main():
    service_1 = get_chat_service()
    service_2 = get_chat_service()

    print("Service type:", type(service_1).__name__)
    print("Same instance:", service_1 is service_2)


if __name__ == "__main__":
    main()