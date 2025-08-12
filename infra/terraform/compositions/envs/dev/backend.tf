terraform {
  # TODO: move to s3
  backend "local" {
    path = "../../../state/dev.tfstate"
  }
}
