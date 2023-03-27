from dynamodb_helper import batch_write_to_dynamodb

async def write_daily_prices(tableName: str, dailyPrices: dict):
    """
    Write a dictionary of daily prices to a DynamoDB table.
    """

    # Define a function to convert daily price to a batch item
    def to_batch_item(dailyPrice):
        return {'PutRequest': {'Item': dailyPrice}}

    # Create a list of batch items using map function
    batch_items = list(map(to_batch_item, dailyPrices))

    # Write batches of 25 to the DynamoDB table using batch_write_to_dynamodb function
    for i in range(0, len(batch_items), 25):
        await batch_write_to_dynamodb(tableName, batch_items[i:i+25])

    # Write any remaining items
    if len(batch_items) % 25 != 0:
        await batch_write_to_dynamodb(tableName, batch_items[-(len(batch_items) % 25):])
