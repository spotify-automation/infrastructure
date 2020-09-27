from typing import Dict, Optional

from aws_cdk.aws_iam import Role, ServicePrincipal, PolicyDocument, PolicyStatement, Effect
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.core import Construct, Duration

__singleton_lambda_role: Optional[Role] = None


def __get_singleton_lambda_role(scope: Construct) -> Role:
    global __singleton_lambda_role
    if not __singleton_lambda_role:
        __singleton_lambda_role = Role(
            scope,
            'LambdaRole',
            assumed_by=ServicePrincipal('lambda.amazonaws.com'),
            inline_policies={
                's3': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            effect=Effect.ALLOW,
                            actions=[
                                's3:ListBucket',
                                's3:PutObject',
                                's3:GetObject',
                                's3:ListObjects'
                            ],
                            resources=[
                                'arn:aws:s3:::*'
                            ]
                        )
                    ]
                ),
                'lambda': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            effect=Effect.ALLOW,
                            actions=['lambda:InvokeFunction'],
                            resources=['arn:aws:lambda:*:*:function:*']
                        )
                    ]
                ),
                'logs': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            effect=Effect.ALLOW,
                            actions=[
                                'logs:CreateLogGroup',
                                'logs:CreateLogStream',
                                'logs:PutLogEvents'
                            ],
                            resources=['*']
                        )
                    ]
                )
            }
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
