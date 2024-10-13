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
  "entries": [
    {
      "response": {
        "content": {
          "text": {
            "banner": {
              "vehicles": [
                {
                  "availability": null,
                  "avgDailyPrice": {
                    "amount": 65.02,
                    "currency": "CAD"
                  },
                  "completedTrips": 5,
                  "estimatedQuote": null,
                  "hostId": 42739272,
                  "id": 2828801,
                  "images": [
                    {
                      "originalImageUrl": "https://images.turo.com/media/vehicle/images/Y3NDCpccT8aC6SZfvYgFbw.jpg",
                      "resizeableUrlTemplate": "https://images.turo.com/media/vehicle/images/Y3NDCpccT8aC6SZfvYgFbw.{width}x{height}.jpg"
                    }
                  ],
                  "isAllStarHost": false,
                  "isFavoritedBySearcher": false,
                  "isNewListing": false,
                  "location": {
                    "city": "Montréal",
                    "country": "CA",
                    "distance": {
                      "unit": "KILOMETERS",
                      "value": 0.16654662357452893
                    },
                    "homeLocation": {
                      "lat": 45.49699343220993,
                      "lng": -73.58466946711803
                    },
                    "isDelivery": false,
                    "locationId": null,
                    "locationSlugs": {
                      "fr_CA": "montreal-qc",
                      "en_GB": "montreal-qc",
                      "en_CA": "montreal-qc",
                      "en_US": "montreal-qc",
                      "en_AU": "montreal-qc",
                      "fr_FR": "montreal-qc"
                    },
                    "state": "QC"
                  },
                  "make": "Tesla",
                  "model": "Model Y",
                  "rating": 5,
                  "seoCategory": "SUV",
                  "tags": [
                    {
                      "label": "Unlimited kilometers",
                      "type": "UNLIMITED_MILEAGE"
                    }
                  ],
                  "type": "SUV",
                  "year": 2024
                }
              ]
            }
          }
        }
      }
    }
  ]
}
```