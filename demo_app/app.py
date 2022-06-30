from h2o_wave import Q, app, handle_on, main, on, ui
import logging


THEMES = [
    'default',
    'h2o-dark',
    'ember',
    'benext',
    'fuchasia',
    'kiwi',
    'lighting',
    'monokai',
    'nature',
    'neon',
    'nord',
    'oceanic',
    'one-dark-pro',
    'solarized',
    'winter-is-coming',
]

@app("/")
async def serve(q: Q):
    try:
        # First time a browser comes to the app
        if not q.client.initialized:
            await init_app(q)
            q.client.initialized = True

        # Other browser interactions
        await handle_on(q)
        await q.page.save()
    except Exception as e: 
        logging.info(e)


async def init_app(q: Q) -> None:
    """Initialize the app for the first page load"""

    # Set Title, Theme, and Layout
    q.page["meta"] = ui.meta_card(
        box="",
        title="Demo App",
        theme="default",
        layouts=[
            ui.layout(
                breakpoint="xs",
                min_height="100vh",
                max_width="1200px",
                zones=[
                    ui.zone("header"),
                    ui.zone(
                        "content",
                        size="1",
                        zones=[
                            ui.zone("vertical", size="1"),
                        ],
                    ),
                    ui.zone(name="footer"),
                ],
            )
        ],
    )

    logo, = await q.site.upload(["static/h2o_logo.svg"])

    # Set Header
    q.page["header"] = ui.header_card(
        box="header",
        title="Demo App",
        subtitle="Now running on Heroku",
        image=logo,
        items=[
            # This button will toggle the theme
            ui.button(
                # A handler (an async function with @on() decorator) must be
                # defined to handle the button click event
                name="change_theme",
                icon="brush",
                label="",
                primary=True
            ),
        ],
        color="transparent",
    )

    # Add main content
    q.page["form"] = ui.form_card(
        box="vertical",
        items=[
            ui.text("Click the brush icon on the Header to change the theme!"),
        ],
    )

    # Set Footer
    q.page["footer"] = ui.footer_card(
        box="footer", caption="Made with 💛 using [H2O Wave](https://wave.h2o.ai)."
    )


@on()
async def change_theme(q: Q):
    """Change the app theme"""
    # Switch theme
    THEMES.append(THEMES.pop(0))

    q.page["meta"].theme = THEMES[0]

