import boto3

dynamodb = boto3.resource("dynamodb")

def write_daily_prices(tableName: str, dailyPrices: dict):
    # initiate batch_items
    batch_items = []
    copied_items = 0
    for dailyPrice in dailyPrices:
        batch_items.append({'PutRequest': {'Item': dailyPrice}})
        copied_items += 1
        # write to destination
        dynamodb.batch_write_item(RequestItems={tableName: batch_items})
        # reset the batch_items after writting
        batch_items = []

    # final write if any items remaining
    if len(batch_items) > 0:
        dynamodb.batch_write_item(RequestItems={tableName: batch_items})
        copied_items += len(batch_items)