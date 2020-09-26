from typing import Dict, Optional

from aws_cdk.aws_iam import Role
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.core import Construct, Duration

from .helpers import get_stack_output

__singleton_lambda_role: Optional[Role] = None


def __get_singleton_lambda_role(scope: Construct) -> Role:
    global __singleton_lambda_role
    if not __singleton_lambda_role:
        __singleton_lambda_role = Role.from_role_arn(
            scope,
            'lambda-role-arn',
            get_stack_output('yahoo-fantasy-football-infrastructure', 'LambdaRoleArn')
        )
    return __singleton_lambda_role


def create_python_function(scope: Construct, _id: str, handler_path: str, environment: Dict[str, str]) -> Function:
    return Function(
        scope,
        _id,
        runtime=Runtime.PYTHON_3_7,
        code=Code.from_asset('.build', exclude=['boto3']),
        handler=handler_path,
        role=__get_singleton_lambda_role(scope),
        environment=environment or {},
        timeout=Duration.minutes(15),
        memory_size=256
    )
