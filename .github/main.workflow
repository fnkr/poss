workflow "Docker" {
  on = "push"
  resolves = [
    "Docker Push",
  ]
}

action "Release?" {
  needs = ["Docker Build", "Docker Login"]
  uses = "actions/bin/filter@master"
  args = "tag"
}

action "Docker Login" {
  uses = "actions/docker/login@master"
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD"]
  env = {
    DOCKER_REGISTRY_URL = "docker.pkg.github.com"
  }
}

action "Docker Build" {
  uses = "actions/docker/cli@master"
  env = {
    DOCKER_REGISTRY_URL = "docker.pkg.github.com"
    PACKAGE_NAME = "poss"
  }
  args = ["build", "-t", "${DOCKER_REGISTRY_URL}/$(printf %s \"$GITHUB_REPOSITORY\" | tr '[:upper:]' '[:lower:]')/${PACKAGE_NAME}:${GITHUB_REF#refs/*/}", "."]
}

action "Docker Push" {
  needs = ["Release?"]
  uses = "actions/docker/cli@master"
  env = {
    DOCKER_REGISTRY_URL = "docker.pkg.github.com"
    PACKAGE_NAME = "poss"
  }
  args = ["push", "${DOCKER_REGISTRY_URL}/$(printf %s \"$GITHUB_REPOSITORY\" | tr '[:upper:]' '[:lower:]')/${PACKAGE_NAME}:${GITHUB_REF#refs/*/}"]
}
