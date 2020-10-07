from os import environ

from aws_cdk.aws_s3 import Bucket, CorsRule, HttpMethods, BucketAccessControl
from aws_cdk.core import Stack, Construct, App, CfnOutput, RemovalPolicy, Environment


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        domain_name = 'aaronmamparo.com'
        pip_hostname = 'spotify-automation.pip.%s' % domain_name
        Bucket(
            self,
            'PipRepositoryBucket',
            bucket_name=pip_hostname,
            public_read_access=True,
            access_control=BucketAccessControl.PUBLIC_READ,
            website_index_document='index.html',
            website_error_document='index.html',
            removal_policy=RemovalPolicy.DESTROY,
            cors=[
                CorsRule(allowed_methods=[HttpMethods.GET], allowed_origins=['*']),
            ]
        )

        CfnOutput(
            self,
            'PipRepositoryHostname',
            value=pip_hostname
        )

        data_lake_bucket = Bucket(
            self,
            'DataLakeBucket',
            removal_policy=RemovalPolicy.DESTROY
        )

        CfnOutput(
            self,
            'DataLakeBucketName',
            value=data_lake_bucket.bucket_name
        )


if __name__ == '__main__':
    app = App()
    MainStack(app, 'spotify-automation-infrastructure', env=Environment(
        account=environ.get('AWS_ACCOUNT_ID'),
        region=environ.get('AWS_DEFAULT_REGION')
    ))
    app.synth()
