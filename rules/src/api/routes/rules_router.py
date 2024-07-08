from fastapi import APIRouter, Depends, HTTPException, status

from common.src.logging.logger import AppLogger
from common.src.queries.api_queries.get_rule import GetRuleQuery
from common.src.validation.rule import Rule
from rules.src.api.dependencies.dependencies import get_rules_handler
from rules.src.api.handlers.rules_handler import RulesHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
	'/get_all_rules/',
	status_code=status.HTTP_200_OK,
	name='Get All Rules',
)
async def get_all_rules():
	try:
		logger.info(f'Fetching all rules')

		logger.info(f'Successfully fetched all rules')
	except HTTPException as e:
		logger.error(f'Error fetching all rules, Error: {str(e)}')
		return {'message': 'Internal server error', 'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@router.get(
	'/get_rule/',
	status_code=status.HTTP_200_OK,
	name='Get Rule',
)
async def get_rule(query: GetRuleQuery = Depends(), rules_handler: RulesHandler = Depends(get_rules_handler)):
	try:
		logger.info(f'Fetching rule by id: {query.name}')
		rule = await rules_handler.get_rule_async(query)
		if rule is None:
			logger.warning(f'Rule not found for id: {query.name}')
			return {'message': 'Rule not found', 'name': query.name}, status.HTTP_204_NO_CONTENT
		logger.info(f'Successfully fetched rule by id: {query.name}')
		return rule
	except HTTPException as e:
		logger.error(f'Error fetching rule by id: {query.name}, Error: {str(e)}')
		return {'message': 'Internal server error', 'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@router.post(
	'/create_rule/',
	status_code=status.HTTP_201_CREATED,
	name='Create Rule',
)
async def create_rule(command: Rule, rules_handler: RulesHandler = Depends(get_rules_handler)):
	try:
		logger.info(f'Creating rule with details: {command.model_dump()}')
		await rules_handler.create_rule_async(command)
		logger.info(f'Successfully created rule: {command.name}')
		return {'message': 'Rule created successfully'}
	except HTTPException as e:
		logger.error(f'Error creating rule {command.name}, Error: {str(e)}')
		return {'message': 'Internal server error', 'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@router.delete(
	'/delete_rule/{rule_id}',
	status_code=status.HTTP_204_NO_CONTENT,
	name='Delete Rule',
)
async def delete_rule(rule_id: str):
	try:
		logger.info(f'Deleting rule by id: {rule_id}')

		logger.info(f'Successfully deleted rule by id: {rule_id}')
	except HTTPException as e:
		logger.error(f'Error deleting rule by id: {rule_id}, Error: {str(e)}')
		return {'message': 'Internal server error', 'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
