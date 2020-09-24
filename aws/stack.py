from aws_cdk.aws_iam import Role, PolicyDocument, PolicyStatement, Effect, ServicePrincipal
from aws_cdk.aws_s3 import Bucket, CorsRule, HttpMethods
from aws_cdk.core import Stack, Construct, App, CfnOutput, RemovalPolicy


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
            'LambdaRoleArn',
            value=lambda_role.role_arn,
            export_name='yahoo-fantasy-football-infrastructure-lambda-role-arn'
        )

        pypi_repository_bucket = Bucket(
            self,
            'PyPIRepositoryBucket',
            bucket_name='pypi-repository-bucket',
            public_read_access=True,
            website_index_document='index.html',
            removal_policy=RemovalPolicy.DESTROY,
            cors=[
                CorsRule(allowed_methods=[HttpMethods.GET], allowed_origins=['*']),
            ]
        )

        CfnOutput(
            self,
            'PyPIRepositoryDomain',
            value=pypi_repository_bucket.bucket_domain_name,
            export_name='yahoo-fantasy-football-infrastructure-pypi-repository-domain'
        )


if __name__ == '__main__':
    app = App()
    MainStack(app, 'yahoo-fantasy-football-infrastructure')
    app.synth()
