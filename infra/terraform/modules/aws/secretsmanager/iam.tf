data "aws_iam_role" "target" {
  name = var.iam_role_name
}

data "aws_iam_policy_document" "read_secret" {
  statement {
    sid     = "AllowReadSecret"
    effect  = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
    ]
    resources = [
      data.aws_secretsmanager_secret.this.arn,
      "${data.aws_secretsmanager_secret.this.arn}*",
    ]
  }
}

resource "aws_iam_policy" "read_secret" {
  name        = "read-secret-${var.secret_name}"
  policy      = data.aws_iam_policy_document.read_secret.json
}

resource "aws_iam_role_policy_attachment" "attach_read_secret" {
  role       = data.aws_iam_role.target.name
  policy_arn = aws_iam_policy.read_secret.arn
}
