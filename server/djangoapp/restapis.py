import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    json_data = ""
    try:
        response = ""
        # Call get method of requests library with URL and parameters
        if api_key:
            # Basic authentication GET
            print("api_key")
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs,
                                     auth=HTTPBasicAuth('apikey', api_key))
        else:
            # no authentication GET
            print("NO api_key")
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except:
        # If any error occurs
        print("Network exception occurred")
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, params):
    try:
        print(url)
        # print(json_payload)
        print(params)
        response = requests.post(url, data=params)
        status_code = response.status_code
        print("post_request With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except:
        # If any error occurs
        print("Network exception occurred")
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # - Call get_request() with specified arguments
    json_result = get_request(url, dealerId=dealer_id)
    # - Parse JSON results into a DealerView object list
    print("get_dealer_reviews_from_cf")
    print(json_result)
    if json_result:
        reviews = json_result["reviews"]
        for review in reviews:
            review_doc = review
            print("before DealerReview")
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"],
                                    purchase=review_doc["purchase"], review=review_doc["review"],
                                    purchase_date="10/20/2020", car_make="Mazda",
                                    car_model="MX-5", car_year=2010,
                                    sentiment="", id=review_doc["id"])
            print("analyze review before")
            sentiment = analyze_review_sentiments(review_obj.review)
            review_obj.sentiment = sentiment
            results.append(review_obj)
    print(results)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    result = "positive"
    print("analyze_review_sentiments")
    print(dealerreview)
    try:
        url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/8f63263b-d006-4a95-9eb9-b711ab4c1ab5"
        api_key = "ZYAIdTw00mh0p1YsJQKaDmHKVNy2FdfR7qF9zZRnUzw8"
        version = "2021-09-01"
        features = "sentiment"
        language = "en"
        text = dealerreview
        print("result start")
        json_result = get_request(url, api_key, version, features, language, text)
        
        print(json_result)
        print("result end")
        result = json_result["sentiment"]["document"]["label"]
        print(result)
    finally:
        return result



