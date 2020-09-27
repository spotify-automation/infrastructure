from aws_cdk.aws_s3 import Bucket, CorsRule, HttpMethods, BucketAccessControl
from aws_cdk.core import Stack, Construct, App, CfnOutput, RemovalPolicy


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        pip_repository_bucket = Bucket(
            self,
            'PipRepositoryBucket',
            bucket_name='daily-fantasy-sports-pip-repository',
            public_read_access=True,
            access_control=BucketAccessControl.PUBLIC_READ,
            website_index_document='index.html',
            removal_policy=RemovalPolicy.DESTROY,
            cors=[
                CorsRule(allowed_methods=[HttpMethods.GET], allowed_origins=['*']),
            ]
        )

        CfnOutput(
            self,
            'PipRepositoryBucketName',
            value=pip_repository_bucket.bucket_name
        )

        CfnOutput(
            self,
            'PipRepositoryDomain',
            value=pip_repository_bucket.bucket_website_domain_name
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
    MainStack(app, 'daily-fantasy-sports-infrastructure')
    app.synth()
