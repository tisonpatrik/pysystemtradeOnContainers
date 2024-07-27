from fastapi import APIRouter, Depends, HTTPException, status

from common.src.logging.logger import AppLogger
from common.src.validation.rule import Rule
from rules.src.api.dependencies.dependencies import get_rules_handler
from rules.src.api.handlers.rules_manager_handler import RulesManagerHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_all_rules/",
    status_code=status.HTTP_200_OK,
    name="Get All Rules",
)
async def get_all_rules(rules_handler: RulesManagerHandler = Depends(get_rules_handler)):
    try:
        logger.info("Fetching all rules")
        rules = await rules_handler.get_all_rules_async()
        if not rules:
            logger.warning("No rules found")
            return {"message": "No rules found"}, status.HTTP_204_NO_CONTENT
        logger.info("Successfully fetched all rules")
        return rules
    except HTTPException as e:
        logger.error(f"Error fetching all rules, Error: {str(e)}")
        return {"message": "Internal server error", "error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@router.post(
    "/create_rule/",
    status_code=status.HTTP_201_CREATED,
    name="Create Rule",
)
async def create_rule(command: Rule = Depends(), rules_handler: RulesManagerHandler = Depends(get_rules_handler)):
    try:
        logger.info(f"Creating rule with details: {command.model_dump()}")
        await rules_handler.create_rule_async(command)
        logger.info(f"Successfully created rule: {command.model_dump()}")
        return {"message": "Rule created successfully"}
    except HTTPException as e:
        logger.error(f"Error creating rule {command.model_dump()}, Error: {str(e)}")
        return {"message": "Internal server error", "error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@router.delete(
    "/delete_rule/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Delete Rule",
)
async def delete_rule(command: Rule = Depends(), rules_handler: RulesManagerHandler = Depends(get_rules_handler)):
    try:
        logger.info(f"Deleting rule with details: {command.model_dump()}")
        await rules_handler.delete_rule_async(command)
        logger.info(f"Successfully deleted rule: {command.model_dump()}")
    except HTTPException as e:
        logger.error(f"Error deleting rule {command.model_dump()}, Error: {str(e)}")
        return {"message": "Internal server error", "error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
