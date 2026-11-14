resource "aws_iam_role_policy" "ec2_backup_upload" {
  name = "eventrush-s3-backup-upload"
  role = aws_iam_role.ec2.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Sid    = "UploadDatabaseBackups"
        Effect = "Allow"

        Action = [
          "s3:PutObject",
          "s3:GetObject"
        ]

        Resource = "${aws_s3_bucket.backups.arn}/database/*"
      }
    ]
  })
}