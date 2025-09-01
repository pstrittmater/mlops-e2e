data "aws_partition" "current" {}

data "aws_iam_role" "target" {
  name = var.iam_role_name
}

locals {
  bucket_arn  = "arn:${data.aws_partition.current.partition}:s3:::${var.bucket_name}"
  objects_arn = "${local.bucket_arn}/*"
}

data "aws_iam_policy_document" "read_bucket" {
  statement {
    sid     = "ReadOnly"
    effect  = "Allow"
    actions = [
      "s3:Get*",
      "s3:List*",
      "s3:Describe*",
      "s3-object-lambda:Get*",
      "s3-object-lambda:List*"
    ]
    resources = [
      local.bucket_arn,
      local.objects_arn,
    ]
  }
}

resource "aws_iam_policy" "read_bucket" {
  name   = "read-bucket-${var.bucket_name}"
  policy = data.aws_iam_policy_document.read_bucket.json
}

resource "aws_iam_role_policy_attachment" "attach_read_bucket" {
  role       = data.aws_iam_role.target.name
  policy_arn = aws_iam_policy.read_bucket.arn
}
