from anime_gui.app import MyApp


def main() -> MyApp:
    return MyApp(
        "My App",
        "com.example.myapp",
    )


if __name__ == "__main__":
    main().main_loop()
