import logging
from fastapi import HTTPException, status

async def execute_with_logging(task, *args, start_msg, end_msg):
    """Helper function to wrap task execution with logging."""
    logging.info(start_msg)
    
    try:
        await task(*args)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while processing the request.")
    
    logging.info(end_msg)
