# Turo Scraper - Product Roadmap

## Initial ideas on how the scraping workflow would work

1. A chrome extension can be used to pull all the available cars from the search page
    - this would post the car IDs to a backend so that we keep track of all available cars in the market
    - we could do a search 2/3 weeks into the future to ensure that as many cars appear in the search (those booked already wouldnt show)
2. A FastAPI backend that can receive data from the various workflows
    - route to ingest car IDs and add them to our watchlist
    - routes to get data about a specific car
3. Scripts that will pull data from turo
    - Other pages, such as car specific pages, expose more detailed data on availability and specs
    - we can use zenrows proxies and scrapers to get those
4. Scripts that will process the data from turo
    - Daily pricing : https://turo.com/api/vehicle/daily_pricing
        - Shows daily pricing. Wether it was a custom price set by owner or suggestion by turo as well as a boolean for car's availability on that day
        - This data can be used to compute occupancy
        - returns data on each of the upcoming 500 days so we need to fugure out a way of processing data in a smart manner
    - Vehicle details: https://turo.com/api/vehicle/detail?
        - exposes details on car's specs and location


## Parsing and loading data from search results

The chrome extension loads all requests that called "https://turo.com/api/v2/search". The returned object contains a key
"vehicles" that has an array of objects, each containing interesting fields about available vehicles such as avgDailyPrice/completedTrips/hostId/id/make/model/type/year/location.city/location.homeLocation.lat/location.homelocation.lng

Exmple data result
```json
{
  "data_type": "Turo Search Page Results",
  "timestamp": "2024-10-13T23:48:54.662Z",
  "entries": [
    {
      "request_method": "POST",
      "request_url": "https://turo.com/api/v2/search",
      "response_status": 200,
      "response_status_text": "",
      "response_content": {
        "banner": {
          "actionText": null,
          "bannerDesign": {
            "animationLoopCount": null,
            "animationURL": null,
            "clickableURL": null,
            "designVariant": null,
            "resizeableIconDarkURL": "https://resources.turo.com/resources/img/banner/thumbs-up-dark__H6f7aeec8335a018494e506131904a399__.jpg",
            "resizeableIconURL": "https://resources.turo.com/resources/img/banner/thumbs-up__H8e2ff43641228b6c6246c70974174b4a__.jpg",
            "withBorder": true
          },
          "bannerName": "CHECKOUT_MORE_THAN_25_HR",
          "text": "Don’t stress: you can cancel your trip for free, up to 24 hours before it starts.",
          "title": null
        },
        "dismissibleBanner": null,
        "makesFilterCount": null,
        "searchId": "9FyJbenr",
        "searchLocation": {
          "appliedRadius": {
            "unit": "MILES",
            "value": 38.2182017975829
          },
          "country": "US",
          "isOperational": true,
          "locationId": null,
          "name": null,
          "point": {
            "lat": 42.4378405,
            "lng": -78.4751945
          },
          "shortName": null,
          "topPois": [],
          "type": "POINT"
        },
        "totalHits": 56,
        "vehicles": [
          {
            "availability": null,
            "avgDailyPrice": {
              "amount": 61.2,
              "currency": "USD"
            },
            "completedTrips": 14,
            "estimatedQuote": null,
            "hostId": 42801905,
            "id": 2706225,
            "images": [
              {
                "originalImageUrl": "https://images.turo.com/media/vehicle/images/Ve-3pJyESBKK7QKKW-O3Og.jpg",
                "resizeableUrlTemplate": "https://images.turo.com/media/vehicle/images/Ve-3pJyESBKK7QKKW-O3Og.{width}x{height}.jpg"
              }
            ],
            "isAllStarHost": false,
            "isFavoritedBySearcher": false,
            "isNewListing": false,
            "location": {
              "city": "Lackawanna",
              "country": "US",
              "distance": {
                "unit": "MILES",
                "value": 32.07219451118512
              },
              "homeLocation": {
                "lat": 42.82337016041945,
                "lng": -78.8265809482411
              },
              "isDelivery": false,
              "locationId": null,
              "locationSlugs": {
                "fr_CA": "lackawanna-ny",
                "en_GB": "lackawanna-ny",
                "en_CA": "lackawanna-ny",
                "en_US": "lackawanna-ny",
                "en_AU": "lackawanna-ny",
                "fr_FR": "lackawanna-ny"
              },
              "state": "NY"
            },
            "make": "Ford",
            "model": "Explorer",
            "rating": 4.9167,
            "seoCategory": "SUV",
            "tags": [],
            "type": "SUV",
            "year": 2021
          }
        ]
      }
    }
  ]
}
```