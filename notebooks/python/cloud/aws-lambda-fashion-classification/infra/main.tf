terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_ecr_repository" "lambda_repo" {
  name                 = "fashion-classification-lambda"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

data "aws_ecr_authorization_token" "ecr" {}

locals {
  app_dir = "${path.module}/../app"

  docker_context_hash = sha256(join("", [
    for f in fileset(local.app_dir, "**") :
    filesha256("${local.app_dir}/${f}")
  ]))
}

provider "docker" {
  registry_auth {
    address  = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com"
    username = data.aws_ecr_authorization_token.ecr.user_name
    password = data.aws_ecr_authorization_token.ecr.password
  }
}

resource "docker_image" "lambda_image" {
  name = "${aws_ecr_repository.lambda_repo.repository_url}:${local.docker_context_hash}"

  build {
    context    = local.app_dir
    dockerfile = "Dockerfile"
    platform   = "linux/amd64"
  }
}

resource "docker_registry_image" "lambda_image" {
  name          = docker_image.lambda_image.name
  keep_remotely = true

  depends_on = [
    docker_image.lambda_image
  ]
}

resource "aws_ecr_lifecycle_policy" "cleanup" {
  repository = aws_ecr_repository.lambda_repo.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 2 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 2
      }
      action = {
        type = "expire"
      }
    }]
  })
}

resource "aws_iam_role" "lambda_role" {
  name = "fashion-classification-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "basic_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


resource "aws_lambda_function" "churn_lambda" {
  function_name = "fashion-classification"
  role          = aws_iam_role.lambda_role.arn

  package_type = "Image"
  image_uri    = docker_registry_image.lambda_image.name

  memory_size = 1024
  timeout     = 30

  depends_on = [
    docker_registry_image.lambda_image
  ]
}

output "lambda_name" {
  value = aws_lambda_function.churn_lambda.function_name
}

output "ecr_repository_url" {
  value = aws_ecr_repository.lambda_repo.repository_url
}
