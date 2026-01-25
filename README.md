# Orna: Record Keeper

This project exists for a couple main reasons, namely:
- More robust storage, easier management, and better visualization of tracked player data
- More streamlined item quality assessment and tracking
- More permanent hub of personal recorded game information

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