from os import environ
from typing import cast

from aws_cdk.aws_route53 import RecordTarget, IAliasRecordTarget, HostedZone, ARecord
from aws_cdk.aws_route53_targets import BucketWebsiteTarget
from aws_cdk.aws_s3 import Bucket, CorsRule, HttpMethods, BucketAccessControl
from aws_cdk.aws_sns import Topic
from aws_cdk.core import Stack, Construct, App, CfnOutput, RemovalPolicy, Environment, Duration


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        domain_name = 'aaronmamparo.com'
        pip_hostname = 'spotify-automation.pip.%s' % domain_name
        pip_repository_bucket = Bucket(
            self,
            'PipRepositoryBucket',
            bucket_name=pip_hostname,
            public_read_access=True,
            access_control=BucketAccessControl.PUBLIC_READ,
            website_index_document='index.html',
            website_error_document='index.html',
            removal_policy=RemovalPolicy.DESTROY,
            cors=[CorsRule(allowed_methods=[HttpMethods.GET], allowed_origins=['*'])]
        )
        ARecord(
            self,
            'PipARecord',
            target=RecordTarget([], cast(IAliasRecordTarget, BucketWebsiteTarget(pip_repository_bucket))),
            zone=HostedZone.from_lookup(self, 'HostedZone', domain_name=domain_name),
            record_name=pip_hostname,
            ttl=Duration.seconds(60)
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

        topic = Topic(
            self,
            'Topic'
        )

        CfnOutput(
            self,
            'TopicArn',
            value=topic.topic_arn
        )




if __name__ == '__main__':
    app = App()
    MainStack(app, 'spotify-automation-infrastructure', env=Environment(
        account=environ.get('AWS_ACCOUNT_ID'),
        region=environ.get('AWS_DEFAULT_REGION')
    ))
    app.synth()
