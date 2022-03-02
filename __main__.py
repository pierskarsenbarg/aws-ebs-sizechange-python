"""An AWS Python Pulumi program"""

from pulumi import ResourceOptions
from pulumi_aws import ec2, ebs

ami = ec2.get_ami(
    filters=[ec2.GetAmiFilterArgs(name="name", values=["amzn-ami-hvm-*"])],
    owners=["137112412989"],
    most_recent=True
)

instance = ec2.Instance("instance",
                        instance_type=ec2.InstanceType.T3A_SMALL,
                        ami=ami.id,
                        subnet_id="subnet-05afcc7bb9112ff6f",
                        opts=ResourceOptions(ignore_changes=["ami"])
                        )

volume = ebs.Volume("volume",
                    availability_zone=instance.availability_zone,
                    size=20,
                    iops=500,
                    type="gp3",
                    throughput=125
                    )

attachment = ec2.VolumeAttachment("attachment",
                                  device_name="/dev/sdb",
                                  instance_id=instance.id,
                                  volume_id=volume.id,
                                  force_detach=True
                                  )
