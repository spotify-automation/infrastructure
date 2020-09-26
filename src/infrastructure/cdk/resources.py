from typing import Dict

from aws_cdk.aws_iam import Role
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.core import Construct, Duration

from .helpers import get_stack_output


def create_python_function(scope: Construct, _id: str, handler_path: str, environment: Dict[str, str]) -> Function:
    return Function(
        scope,
        _id,
        runtime=Runtime.PYTHON_3_7,
        code=Code.from_asset('.build', exclude=['boto3']),
        handler=handler_path,
        role=Role.from_role_arn(get_stack_output('yahoo-fantasy-football-infrastructure', 'LambdaRoleArn')),
        environment=environment or {},
        timeout=Duration.minutes(15),
        memory_size=256
    )