from aws_cdk.aws_iam import Role, PolicyDocument, PolicyStatement, Effect, ServicePrincipal
from aws_cdk.core import Stack, Construct, App, CfnOutput


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        lambda_role = Role(
            self,
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

        CfnOutput(
            self,
            'lambda-role-arn',
            value=lambda_role.role_arn,
            export_name='yahoo-fantasy-football-infrastructure-lambda-role-arn'
        )


if __name__ == '__main__':
    app = App()
    MainStack(app, 'yahoo-fantasy-football-infrastructure')
    app.synth()
