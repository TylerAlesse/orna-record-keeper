# Orna: Record Keeper

This project exists for a couple main reasons, namely:
- More robust storage, easier management, and better visualization of tracked player data
- More streamlined item quality assessment and tracking
- More permanent hub of personal recorded game information

The [EXP-Less Record Keeping](https://docs.google.com/spreadsheets/d/1PX9VeuRx6Kli0Ln_jIN8vZNA9oD4Whd2772TXT-DwZg/edit?usp=sharing) spreadsheet is one of the two projects that the [Record Keeper] is meant to replace almost in its entirety. There are multiple sub-sections that are centered around active data gathering and analysis of the game, rather than specifically for the character itself, such as the:
- Deep Dungeon Data
- Monument Data
- Citadel Data
- Arena Data
As such, those section will not be ported into this project, as the spreadsheet format lends itself well to the more dynamic nature of the analysis.

The [Sell Prince Research Center (SPRC)](https://docs.google.com/spreadsheets/d/1z3RMf8kj1VY5zK7fOdcS9fzwTy5RWlYLlBkzQp4QKWI/edit?usp=sharing) is the other major project that the [Record Keeper] intends to, at least partially, replace. By having the SPRC incorporated into the Record Keeper, the means of keeping an accurate inventory of the character documented goes up substantially compared to the existing workflow of needing to compare data across two spreadsheets. Additional features from the SPRC can be added to the Record Keeper in the future, as needed.

## Database and API

Originally, the data was stored via Google Sheets. This allowed for easy editing both on desktop, for more serious editing, and via mobile-app, for quick on-the-go data entry. This approach, while difficult to make visually interesting, allowed for easy data entry, did not require handling security, and did not cost money.

The API will be capable of handling both read and write requests to the DB, but will only be accessible locally. While this cuts off the ability for querying on other devices, this mitigates some of the need to do authorization for API requests that modify the DB.

## Web Interface

While the DB file could certainly be modified with your preferred DBMS or via API calls, the main method of viewing, adding, and removing data will be through the web interface. There will be the option to export static pages, to allow for hosting snapshops of the data on whatever service you need, removing the need for authorization for API calls.

### Main Pages
- __Player Data__: Current and historical Player Record data, including Guild EXP.
- __Item Collection__: Virtual display case of the highest quality equipment and count of total items collected.
- __Monster Collection__: Codex Completion status, Traveler's Guild Manifests, and Kill Counts for Monsters, Bosses, and some Raids.
- __Item Assessment Hub__: Assessment tool for determining Item Quality via Gold Value when selling to an in-game shop.